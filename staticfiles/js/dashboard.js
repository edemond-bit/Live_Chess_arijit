$(function() {
    var engine = new Worker("/static/js/stockfish.js");
    console.log("GUI: uci");
    engine.postMessage("uci");
    console.log("GUI: ucinewgame");
    engine.postMessage("ucinewgame");

    var moveList = ['d3', 'e5', 'e3', 'd5', 'f3', 'Nc6', 'g3', 'Nf6', 'h3', 'd4', 'c3', 'dxc3'];

    // console.log(moveList.length - 1);
    var scoreList = [];
    var cursor = 0;


    //alert(4);
    //goToMove(0);



    var player = 'w';
    var entirePGN = ''; // longer than current PGN when rewind buttons are clicked

    var board;
    var game = new Chess(), // move validation, etc.
        statusEl = $('#status'),
        fenEl = $('#fen'),
        pgnEl = $('#pgn');
    pgnEll = $('#pgn1');
    var whiteSquareGrey = '#a9a9a9';
    var blackSquareGrey = '#696969';
    // true for when the engine is processing; ignore_mouse_events is always true if this is set (also during animations)
    var engineRunning = false;

    // don't let the user press buttons while other button clicks are still processing
    var board3D = ChessBoard3.webGLEnabled();

    if (!board3D) {
        swal("WebGL unsupported or disabled.", "Using a 2D board...");
        $('#dimensionBtn').remove();
    }

    var scoreGauge = $('#gauge').SonicGauge({
        label: 'WHITE\'S ADVANTAGE\n(centipawns)',
        start: {
            angle: -230,
            num: -2000
        },
        end: {
            angle: 50,
            num: 2000
        },
        markers: [{
            gap: 200,
            line: {
                "width": 11,
                "stroke": "none",
                "fill": "#cccccc"
            },
            text: {
                "space": -20,
                "text-anchor": "middle",
                "fill": "#cccccc",
                "font-size": 8
            }
        }, {
            gap: 100,
            line: {
                "width": 9,
                "stroke": "none",
                "fill": "#999999"
            }
        }, {
            gap: 50,
            line: {
                "width": 7,
                "stroke": "none",
                "fill": "#888888"
            }
        }],
        animation_speed: 200,
        diameter: 250,
        style: {
            label: {
                "font-size": 9,
                fill: '#cccccc'
            },
            center: {
                fill: 'r#f46a3a-#890b0b'
            },
            outline: {
                fill: 'r#888888-#000000',
                stroke: 'black',
                'stroke-width': 1
            }
        }
    });


    function updateScoreGauge(score) {
        document.getElementById('setVal').value = score;

        var $p = $('.progress1');
        var $input = $('input');

        if (score >= 0) {

            if (score <= 2500 && score > 0) {

                $p.css({
                    width: 180 + score + 'px',
                    backgroundPosition: score + 'px'
                });
            }
        }
        if (score < 0) {

            if (score < 0 && score > -2500) {
                if (score > -180) {
                    var tt = (180) + (score);


                } else {
                    var t = (180) + (score);
                    var tt = 180 + (t);


                }
                $p.css({

                    width: tt + 'px',
                    backgroundPosition: tt + 'px'
                });
            }
        }




        scoreGauge.SonicGauge('val', parseInt(score, 10));
    }




    function adjustBoardWidth() {
        var fudge = 250;
        var windowWidth = $(window).width();
        var windowHeight = $(window).height();
        var desiredBoardWidth = $('.one1').outerWidth(true);
        var desiredBoardHeight = windowHeight - $('#header').outerHeight(true) - $('#banner').outerHeight(true) - $('#footer').outerHeight(true) - fudge;

        var boardDiv = $('#board');
        if (board3D) {
            // Using chessboard3.js.
            // Adjust for 4:3 aspect ratio
            desiredBoardWidth &= 0xFFFC; // mod 4 = 0
            desiredBoardHeight -= (desiredBoardHeight % 3); // mod 3 = 0
            if (desiredBoardWidth * 0.75 > desiredBoardHeight) {
                desiredBoardWidth = desiredBoardHeight * 4 / 3;
            }
            boardDiv.css('width', '80%');
            boardDiv.css('height', '100%');

        } else {
            // This is a chessboard.js board. Adjust for 1:1 aspect ratio
            desiredBoardWidth = Math.min(desiredBoardWidth, desiredBoardHeight);
            boardDiv.css('width', '80%');
            boardDiv.css('height', '65%');
        }
        if (board !== undefined) {
            board.resize();
        }
    }

    function fireEngine() {
        engineRunning = true;
        updateStatus();
        var currentScore;
        var msg = "position fen " + game.fen();
        //console.log("GUI: " + msg);
        engine.postMessage(msg);
        msg = 'go movetime ' + $('#moveTime').val();
        //console.log("GUI: " + msg);
        engine.postMessage(msg);
        engine.onmessage = function(event) {
            var line = event.data;

            //console.log("ENGINE: " + line);
            var best = parseBestMove(line);
            if (best !== undefined) {
                var move = game.move(best);
                moveList.push(move);
                //console.log(moveList);



                //var gameMoves = moveList.replace(/\[(.*?)\]/gm, '').replace(h.Result, '').trim();
                //console.log(gameMoves);
                if (currentScore !== undefined) {
                    if (scoreList.length > 0) {
                        scoreList.pop(); // remove the dummy score for the user's prior move
                        scoreList.push(currentScore); // Replace it with the engine's opinion
                    }
                    scoreList.push(currentScore); // engine's response
                } else {
                    scoreList.push(0); // not expected
                }
                cursor++;
                board.position(game.fen(), true);
                engineRunning = false;
                updateStatus();
            } else {
                // Before the move gets here, the engine emits info responses with scores
                var score = parseScore(line);
                if (score !== undefined) {
                    if (player === 'w') {
                        score = -score; // convert from engine's score to white's score
                    }
                    updateScoreGauge(score);
                    currentScore = score;
                }
            }
        };
    }



    function parseBestMove(line) {
        var match = line.match(/bestmove\s([a-h][1-8][a-h][1-8])(n|N|b|B|r|R|q|Q)?/);
        if (match) {
            var bestMove = match[1];
            var promotion = match[2];
            return {
                from: bestMove.substring(0, 2),
                to: bestMove.substring(2, 4),
                promotion: promotion
            }
        }
    }

    function parseScore(line) {
        var match = line.match(/score\scp\s(-?\d+)/);
        if (match) {
            return match[1];
        } else {
            if (line.match(/mate\s-?\d/)) {
                return 2500;
            }
        }
    }






    function updateStatus() {

        var status = '';

        var moveColor = 'White';
        if (game.turn() === 'b') {
            moveColor = 'Black';
        }

        if (game.game_over()) {

            if (game.in_checkmate()) {
                status = moveColor + ' checkmated.';
            } else if (game.in_stalemate()) {
                status = moveColor + " stalemated";
            } else if (game.insufficient_material()) {
                status = "Draw (insufficient material)."
            } else if (game.in_threefold_repetition()) {
                status = "Draw (threefold repetition)."
            } else if (game.in_draw()) {
                status = "Game over (fifty move rule)."
            }
            swal({
                title: "Game Over",
                text: status,
                type: 'info',
                showCancelButton: false,
                confirmButtonColor: "#DD6655",
                onConfirmButtonText: 'OK',
                closeOnConfirm: true
            });
            engineRunning = false;
        }

        // game still on
        else {
            if (player === 'w') {
                status = "Computer playing Black; ";
            } else {
                status = "Computer playing White; ";
            }
            status += moveColor + ' to move.';

            // check?
            if (game.in_check() === true) {
                status += ' ' + moveColor + ' is in check.';
            }
        }

        fenEl.html(game.fen().replace(/ /g, '&nbsp;'));
        var currentPGN = game.pgn({
            max_width: 10,
            newline_char: "<br>"
        });
        //console.log(entirePGN);
        var matches = entirePGN.lastIndexOf(currentPGN, 0) === 0;
        if (matches) {
            currentPGN += "<span>" + entirePGN.substring(currentPGN.length, entirePGN.length) + "</span>";
        } else {
            entirePGN = currentPGN;
        }
        //pgnEl.html(currentPGN);

        //pgnEl.html(currentPGN);


        if (engineRunning) {
            // status += ' Thinking...';
            status += ' ';
        }
        //pgnEll.html(currentPGN);
        if (engineRunning) {
            // status += ' Thinking...';
            status += ' ';
        }
        statusEl.html(status);
    };




    // Set up chessboard
    var onDrop = function(source, target) {

        if (engineRunning) {
            return 'snapback';
        }

        if (board.hasOwnProperty('removeGreySquares') && typeof board.removeGreySquares === 'function') {
            board.removeGreySquares();
        }

        // see if the move is legal
        var move = game.move({
            from: source,
            to: target,
            promotion: 'q' //$("#promotion").val()
        });



        // illegal move
        if (move === null) return 'snapback';
        // highlight black's move

        removeHighlights('white')
        $board.find('.square-' + source).addClass('highlight-white')
        $board.find('.square-' + target).addClass('highlight-white')

        if (cursor === 0) {
            console.log("GUI: ucinewgame");
            engine.postMessage("ucinewgame");
        }
        moveList = moveList.slice(0, cursor);
        scoreList = scoreList.slice(0, cursor);
        moveList.push(move);
        // User just made a move- add a dummy score for now. We will correct this element once we hear from the engine
        scoreList.push(scoreList.length === 0 ? 0 : scoreList[scoreList.length - 1]);
        cursor = moveList.length;
        //console.log(cursor);
    };


    var $board = $('#board')
    var squareClass = 'square-55d63'

    function removeHighlights(color) {
        $board.find('.' + squareClass)
            .removeClass('highlight-' + color)
    }
    // update the board position after the piece snap
    // for castling, en passant, pawn promotion
    var onSnapEnd = function() {

        if (!game.game_over() && game.turn() !== player) {
            fireEngine();
        }

    };

    var squareToHighlight = null

    function onMouseoverSquare(square, piece) {
        // get list of possible moves for this square
        var moves = game.moves({
            square: square,
            verbose: true
        })

        // exit if there are no moves available for this square
        if (moves.length === 0) {
            ondragpostion(square);
        }

        // highlight the square they moused over
        greySquare(square)

        // highlight the possible squares for this piece
        for (var i = 0; i < moves.length; i++) {
            board.addArrowAnnotation(square, moves[i].to)
            greySquare(moves[i].to)
        }
    }

    $('input[type="checkbox"][name="btn_drawar"]').change(function() {

        if (this.checked) {

            $('#imageView').css('display', 'initial');
            $('#imageTemp').css('display', 'initial');
            $('#imageView').css('z-index', 1);
            $('#imageTemp').css('z-index', 11);
            $('#board').css('z-index', -1111);
        } else {

            $('#imageView').css('display', 'none');
            $('#imageView').css('z-index', -1);
            $('#imageTemp').css('z-index', -11);
            $('#board').css('z-index', 1111);
        }
    });

    function ondragpostion(square) {
        //board.addArrowAnnotation(square, "h5"); 
    }

    function onMouseoutSquare(square, piece) {
        board.clearAnnotation()
        removeGreySquares()
    }

    function removeGreySquares() {
        $('#board .square-55d63').css('background', '')
    }

    function greySquare(square) {
        // alert(square);
        var square = $('#board .square-' + square)

        var background = whiteSquareGrey
        if (square.hasClass('black-3c85d')) {
            background = blackSquareGrey
        }

        square.css('background', background)


    }



    function onMoveEnd() {
        $board.find('.square-' + squareToHighlight)
            .addClass('highlight-black')
    }

    function createBoard(pieceSet, args, args1, args2) {
        // alert(pieceSet+"->"+args);
        var cfg = {

            cameraControls: true,
            draggable: true,
            position: 'r1bqkb1r/ppp2ppp/2n2n2/4p3/8/2pPPPPP/PP6/RNBQKBNR w KQkq - 0 7',
            onDrop: onDrop,
            onMouseoutSquare: onMouseoutSquare,
            onMouseoverSquare: onMouseoverSquare,
            onSnapEnd: onSnapEnd,
            onMoveEnd: onMoveEnd,
            overlay: true
        };


        //goToMove(moveList.length - 1);
        // if (board3D) {
        //     if (pieceSet) {
        //         if (pieceSet === 'minions') {
        //             cfg.whitePieceColor = 0xFFFF00;
        //             cfg.blackPieceColor = 0xCC00CC;
        //             cfg.lightSquareColor = 0x888888;
        //             cfg.darkSquareColor = 0x666666;
        //         }
        //         cfg.pieceSet = '/static/assets/chesspieces/' + pieceSet + '/{piece}.json';
        //     }
        //     return new ChessBoard3('board', cfg);
        //   } else {

        if (args == '2D') {
            if (args1 == 'piece') {
                var selectedVal = $("#board-style option:selected").val();
                if (selectedVal == 'aluminium') {

                    // cfg.boardTheme = ["#6fadd4", "#d0ceca"];
                    return new ChessBoard('board', {
                        pieceTheme: '/static/img/chesspieces/' + pieceSet + '/{piece}.png',
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/ab.png')", "url('/static/img/chesspieces/board/aw.png')", "url('/static/img/chesspieces/board/ab.png')"]

                    });


                }
                if (selectedVal == 'cherry') {

                    //cfg.boardTheme = ["#521b01", "#b45119"];
                    return new ChessBoard('board', {
                        pieceTheme: '/static/img/chesspieces/' + pieceSet + '/{piece}.png',
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/cherry1.png')", "url('/static/img/chesspieces/board/cherry2.png')", "url('/static/img/chesspieces/board/cherry2.png')"]

                    });
                }
                if (selectedVal == 'lapis') {

                    //cfg.boardTheme = ["#244251", "#c9b46b"];
                    return new ChessBoard('board', {
                        pieceTheme: '/static/img/chesspieces/' + pieceSet + '/{piece}.png',
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/wb.png')", "url('/static/img/chesspieces/board/ww.png')", "url('/static/img/chesspieces/board/wb.png')"]

                    });
                }
                if (selectedVal == 'marble') {

                    //cfg.boardTheme = ["#bb886e", "#e9d2b7"];
                    return new ChessBoard('board', {
                        pieceTheme: '/static/img/chesspieces/' + pieceSet + '/{piece}.png',
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/marble1.png')", "url('/static/img/chesspieces/board/marble2.png')", "url('/static/img/chesspieces/board/marble1.png')"]

                    });
                }
                if (selectedVal == 'sand') {

                    //cfg.boardTheme = ["#c8a97d", "#fdedb7"];
                    return new ChessBoard('board', {
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/sand1.png')", "url('/static/img/chesspieces/board/sand2.png')", "url('/static/img/chesspieces/board/sand1.png')"],
                        pieceTheme: '/static/img/chesspieces/' + pieceSet + '/{piece}.png'
                    });
                }
                if (selectedVal == 'slate') {

                    //cfg.boardTheme = ["#8c8c8c", "#c9c9c9"];
                    return new ChessBoard('board', {
                        pieceTheme: '/static/img/chesspieces/' + pieceSet + '/{piece}.png',
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/slate1.png')", "url('/static/img/chesspieces/board/slate2.png')", "url('/static/img/chesspieces/board/slate2.png')"]

                    });
                } else {
                    //cfg.boardTheme = ["#ae6c37", "#d4b171"];#244251", "#c9b46b

                    return new ChessBoard('board', {
                        pieceTheme: '/static/img/chesspieces/' + pieceSet + '/{piece}.png',

                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/lapis/lapis1.png')", "url('/static/img/chesspieces/board/lapis/lapis2.png')", "url('/static/img/chesspieces/board/lapis/lapis2.png')"]


                    });
                }



                //cfg.pieceTheme = '/static/img/chesspieces/' + pieceSet + '/{piece}.png';


                //return new ChessBoard('board', cfg);
            }
            if (args1 == 'board') {
                if (pieceSet == 'aluminium') {
                    // cfg.boardTheme = ["#6fadd4", "#d0ceca"];

                    return new ChessBoard('board', {
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/ab.png')", "url('/static/img/chesspieces/board/aw.png')", "url('/static/img/chesspieces/board/ab.png')"]

                    });

                }
                if (pieceSet == 'cherry') {

                    //cfg.boardTheme = ["#521b01", "#b45119"];
                    return new ChessBoard('board', {
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/cherry1.png')", "url('/static/img/chesspieces/board/cherry2.png')", "url('/static/img/chesspieces/board/cherry2.png')"]

                    });
                }
                if (pieceSet == 'lapis') {

                    //cfg.boardTheme = ["#244251", "#c9b46b"];
                    return new ChessBoard('board', {
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/wb.png')", "url('/static/img/chesspieces/board/ww.png')", "url('/static/img/chesspieces/board/wb.png')"]

                    });
                }
                if (pieceSet == 'marble') {

                    //cfg.boardTheme = ["#bb886e", "#e9d2b7"];
                    return new ChessBoard('board', {
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/marble1.png')", "url('/static/img/chesspieces/board/marble2.png')", "url('/static/img/chesspieces/board/marble1.png')"]

                    });
                }
                if (pieceSet == 'sand') {

                    //cfg.boardTheme = ["#c8a97d", "#fdedb7"];
                    return new ChessBoard('board', {
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/sand1.png')", "url('/static/img/chesspieces/board/sand2.png')", "url('/static/img/chesspieces/board/sand1.png')"]

                    });
                }
                if (pieceSet == 'slate') {

                    //cfg.boardTheme = ["#8c8c8c", "#c9c9c9"];
                    return new ChessBoard('board', {
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/slate1.png')", "url('/static/img/chesspieces/board/slate2.png')", "url('/static/img/chesspieces/board/slate2.png')"]

                    });
                }
                return new ChessBoard('board', cfg);
            }

        } else {
            //cfg.boardTheme = ["#ae6c37", "#d4b171"];#244251", "#c9b46b

            return new ChessBoard('board', {
                draggable: true,
                position: 'start',
                onDrop: onDrop,
                onSnapEnd: onSnapEnd,
                boardTheme: ["url('/static/img/chesspieces/board/lapis/lapis1.png')", "url('/static/img/chesspieces/board/lapis/lapis2.png')", "url('/static/img/chesspieces/board/lapis/lapis2.png')"]


            });
        }

        // }
    }


    adjustBoardWidth();
    board = createBoard();

    $(window).resize(function() {
        adjustBoardWidth();
    });
    //console.log(board.position());





    var onChange = function onChange() { //fires when the board position changes
            //highlight the current move
            $("[class^='gameMove']").removeClass('highlight');
            $('.gameMove' + cursor).addClass('highlight');
        }
        // Set up buttons
    $('#startBtn').on('click', function() {
        var cursorStart = 0;
        if (player === 'b') {
            cursorStart = 1;
        }
        while (cursor > cursorStart) {
            game.undo();
            cursor--;
        }
        updateScoreGauge(0);
        board.position(game.fen());
        updateStatus();
    });
    $('#backBtn').on('click', function() {
        if (cursor > 0) {
            cursor--;
            game.undo();
            board.position(game.fen());
            var score = cursor === 0 ? 0 : scoreList[cursor - 1];
            updateScoreGauge(score);
            updateStatus();
        }
    });
    $('#forwardBtn').on('click', function() {
        if (cursor < moveList.length) {
            game.move(moveList[cursor]);
            var score = scoreList[cursor];
            updateScoreGauge(score);
            board.position(game.fen());
            cursor++;
            updateStatus();
        }
    });




    var cursorStart1 = 0;
    var pause_value = "play";
    $('#playBtn').on('click', function() {
        pause_value = "play";
        //cursorStart=0;
        while (cursor > cursorStart1) {
            game.undo();
            cursor--;
        }
        updateScoreGauge(0);
        board.position(game.fen());
        updateStatus();
        if (pause_value == "play") {
            play();
        } else {
            if (pause_value == "pause") {
                stop();
            } else {
                return;
            }
        }

    });

    function play() {
        var k = moveList.length;
        document.getElementById('movecount').value = k;
        // var pause = document.getElementById('playcount').value;
        var me = this;
        var delay = 1000;
        var timerId = null;
        var moveId = 0;
        for (i = k; i > 0; i--) {
            document.getElementById('movecount').value = i;
            setTimeout(function timer() {
                if (pause_value == 'pause') {

                } else {

                    game.move(moveList[cursor]);
                    var score = scoreList[cursor];
                    board.position(game.fen());
                    cursor++;
                    updateStatus();
                    updateScoreGauge(score);
                }

            }, i * delay);
            cursorStart1++;

        }


    }
    $('#pause').on('click', function() {
        pause_value = "pause";
        document.getElementById("board").disabled = true;
        if (pause_value == "play") {
            play();
        } else {
            //pause_value="play";
        }

    });

    function stop() {}
    $('#endBtn').on('click', function() {
        while (cursor < moveList.length) {
            game.move(moveList[cursor++]);
        }
        board.position(game.fen());
        updateScoreGauge(scoreList.length == 0 ? 0 : scoreList[cursor - 1]);
        updateStatus();
    });
    $('#hintBtn').on('click', function() {
        if (game.turn() === player) {
            engineRunning = true;
            var msg = "position fen " + game.fen();
            console.log("GUI: " + msg);
            engine.postMessage(msg);
            msg = 'go movetime ' + $('#moveTime').val();
            console.log(msg);
            engine.postMessage(msg);
            engine.onmessage = function(event) {
                console.log("ENGINE: " + event.data);
                var best = parseBestMove(event.data);
                if (best !== undefined) {
                    var currentFEN = game.fen();
                    game.move(best);
                    var hintedFEN = game.fen();
                    game.undo();
                    board.position(hintedFEN, true);
                    // give them a second to look before sliding the piece back
                    setTimeout(function() {
                        board.position(currentFEN, true);
                        engineRunning = false;
                    }, 1000); // give them a second to look
                }
            }
        }
    });
    $('#flipBtn').on('click', function() {
        if (game.game_over()) {
            return;
        }
        board.flip(); //wheeee!
        if (player === 'w') {
            player = 'b';
        } else {
            player = 'w';
        }
        updateStatus();
        setTimeout(fireEngine, 1000);
    });

    $('#dimensionBtn').on('click', function() {
        var dimBtn = $("#dimensionBtn");
        var sel = document.getElementById('dimensionBtn').value;
        dimBtn.prop('disabled', true);
        var position = board.position();
        var orientation = board.orientation();
        board.destroy();
        board3D = !board3D;
        adjustBoardWidth();
        if (sel == '3D') {

            dimBtn.val(board3D ? '3D' : '2D');
            setTimeout(function() {

                board = createBoard($('#piecesMenu').val(), sel);
                board.orientation(orientation);
                board.position(position);
                $("#dimensionBtn").prop('disabled', false);
            });
        }
        if (sel == '2D') {
            setTimeout(function() {

                board = createBoard($('#piece-style').val(), sel);
                console.log(board);
                board.orientation(orientation);
                board.position(position);
                $("#dimensionBtn").prop('disabled', false);

            });
        }


    });


    $("#setFEN").on('click', function(e) {
        swal({
            title: "SET FEN",
            text: "Enter a FEN position below:",
            type: "input",
            inputType: "text",
            showCancelButton: true,
            closeOnConfirm: false
        }, function(fen) {
            if (fen === false) {
                return; //cancel
            }
            fen = fen.trim();
            console.log(fen);
            var fenCheck = game.validate_fen(fen);
            console.log("valid: " + fenCheck.valid);
            if (fenCheck.valid) {
                game = new Chess(fen);
                console.log("GUI: ucinewgame");
                engine.postMessage('ucinewgame');
                console.log("GUI: position fen " + fen);
                engine.postMessage('position fen ' + fen);
                board.position(fen);
                fenEl.val(fen);
                pgnEl.empty();
                pgnEll.empty();
                updateStatus();
                swal("Success", "FEN parsed successfully.", "success");
            } else {
                console.log(fenCheck.error);
                swal.showInputError("ERROR: " + fenCheck.error);
                return false;
            }
        });
    });

    $("#setPGN").on('click', (function(e) {
        swal({
            title: "SET PGN",
            text: "Enter a game PGN below:",
            type: "input",

            showCancelButton: true,
            closeOnConfirm: false
        }, function(pgn) {
            if (pgn === false) {
                return; // cancel
            }
            pgn = pgn.trim();
            console.log(pgn);
            var pgnGame = new Chess();
            if (pgnGame.load_pgn(pgn)) {
                game = pgnGame;
                var fen = game.fen();
                console.log("GUI: ucinewgame");
                engine.postMessage('ucinewgame');
                console.log("GUI: position fen " + fen);
                engine.postMessage('position fen ' + game.fen());
                board.position(fen, false);
                fenEl.val(game.fen());
                pgnEl.empty();
                pgnEll.empty();
                moveList = game.history();
                scoreList = [];
                for (var i = 0; i < moveList.length; i++) {
                    scoreList.push(0);
                }
                cursor = moveList.length;
                updateStatus();
                swal("Success", "PGN parsed successfully.", "success");
            } else {
                swal.showInputError("PGN not valid.");
                return false;
            }
        });
    }));

    $("#resetBtn").on('click', function(e) {
        player = 'w';
        game = new Chess();
        fenEl.empty();
        pgnEl.empty();
        pgnEll.empty();
        largestPGN = '';
        moveList = [];
        scoreList = [];
        cursor = 0;
        board.start();
        board.orientation('white');
        console.log("GUI: ucinewgame");
        engine.postMessage('ucinewgame');
        updateScoreGauge(0);
    });

    $("#engineMenu").change(function() {
        console.log($("#engineMenu").val());
        if (engine) {
            var jsURL = $("#engineMenu").val();
            engine.terminate();
            engine = new Worker(jsURL);
            console.log("GUI: uci");
            engine.postMessage('uci');
            console.log("GUI: ucinewgame");
            engine.postMessage('ucinewgame');
            updateScoreGauge(0); // they each act a little differently
            if (jsURL.match(/p4wn/)) {
                swal('Using the tiny p4wn engine, which plays at an amateur level.');
            } else if (jsURL.match(/lozza/)) {
                swal('Using Lozza engine by Colin Jerkins, estimated rating 2340.')
            } else if (jsURL.match(/stockfish/)) {
                swal("Using stockfish engine, estimated rating > 3000.");
            }
        }
    });

    $('#piecesMenu').change(function() {
        var fen = board.position();
        board.destroy();
        board = createBoard($('#piecesMenu').val(), '3D', '');
        board.position(fen);
        adjustBoardWidth();
    });

    $('#piece-style').change(function() {
        var fen = board.position();
        board.destroy();
        board = createBoard($('#piece-style').val(), '2D', 'piece');
        board.position(fen);
        adjustBoardWidth();
    });
    $('#board-style').change(function() {
        var fen = board.position();
        board.destroy();
        board = createBoard($('#board-style').val(), '2D', 'board');
        board.position(fen);
        adjustBoardWidth();
    });

    updateStatus();

});


function onChooseFile(event, onLoadFileHandler) {
    if (typeof window.FileReader !== 'function')
        throw ("The file API isn't supported on this browser.");
    let input = event.target;
    if (!input)
        throw ("The browser does not properly implement the event object");
    if (!input.files)
        throw ("This browser does not support the `files` property of the file input.");
    if (!input.files[0])
        return undefined;
    let file = input.files[0];
    let fr = new FileReader();
    fr.onload = onLoadFileHandler;
    fr.readAsText(file);
}


function onFileLoad(elementId, event, args) {
    var engine = new Worker("/static/js/stockfish.js");
    console.log("GUI: uci");
    engine.postMessage("uci");
    console.log("GUI: ucinewgame");
    engine.postMessage("ucinewgame");

    var moveList = [],
        scoreList = [];

    var cursor = 0;

    var player = 'w';
    var entirePGN = ''; // longer than current PGN when rewind buttons are clicked

    var board;
    var game = new Chess(), // move validation, etc.
        statusEl = $('#status'),
        fenEl = $('#fen'),
        pgnEl = $('#pgn');
    pgnEll = $('#pgn1');
    var whiteSquareGrey = '#a9a9a9';
    var blackSquareGrey = '#696969';
    // true for when the engine is processing; ignore_mouse_events is always true if this is set (also during animations)
    var engineRunning = false;

    // don't let the user press buttons while other button clicks are still processing
    var board3D = ChessBoard3.webGLEnabled();

    if (!board3D) {
        swal("WebGL unsupported or disabled.", "Using a 2D board...");
        $('#dimensionBtn').remove();
    }

    var scoreGauge = $('#gauge').SonicGauge({
        label: 'WHITE\'S ADVANTAGE\n(centipawns)',
        start: {
            angle: -230,
            num: -2000
        },
        end: {
            angle: 50,
            num: 2000
        },
        markers: [{
            gap: 200,
            line: {
                "width": 11,
                "stroke": "none",
                "fill": "#cccccc"
            },
            text: {
                "space": -20,
                "text-anchor": "middle",
                "fill": "#cccccc",
                "font-size": 8
            }
        }, {
            gap: 100,
            line: {
                "width": 9,
                "stroke": "none",
                "fill": "#999999"
            }
        }, {
            gap: 50,
            line: {
                "width": 7,
                "stroke": "none",
                "fill": "#888888"
            }
        }],
        animation_speed: 200,
        diameter: 250,
        style: {
            label: {
                "font-size": 9,
                fill: '#cccccc'
            },
            center: {
                fill: 'r#f46a3a-#890b0b'
            },
            outline: {
                fill: 'r#888888-#000000',
                stroke: 'black',
                'stroke-width': 1
            }
        }
    });

    function updateScoreGauge(score) {
        document.getElementById('setVal').value = score;

        var $p = $('.progress1');
        var $input = $('input');

        if (score >= 0) {

            if (score <= 2500 && score > 0) {

                $p.css({
                    width: 180 + score + 'px',
                    backgroundPosition: score + 'px'
                });
            }
        }
        if (score < 0) {

            if (score < 0 && score > -2500) {
                if (score > -180) {
                    var tt = (180) + (score);


                } else {
                    var t = (180) + (score);
                    var tt = 180 + (t);


                }
                $p.css({

                    width: tt + 'px',
                    backgroundPosition: tt + 'px'
                });
            }
        }




        scoreGauge.SonicGauge('val', parseInt(score, 10));
    }

    function adjustBoardWidth() {
        var fudge = 250;
        var windowWidth = $(window).width();
        var windowHeight = $(window).height();
        var desiredBoardWidth = $('.one1').outerWidth(true);
        var desiredBoardHeight = windowHeight - $('#header').outerHeight(true) - $('#banner').outerHeight(true) - $('#footer').outerHeight(true) - fudge;

        var boardDiv = $('#board');
        if (board3D) {
            // Using chessboard3.js.
            // Adjust for 4:3 aspect ratio
            desiredBoardWidth &= 0xFFFC; // mod 4 = 0
            desiredBoardHeight -= (desiredBoardHeight % 3); // mod 3 = 0
            if (desiredBoardWidth * 0.75 > desiredBoardHeight) {
                desiredBoardWidth = desiredBoardHeight * 4 / 3;
            }
            boardDiv.css('width', '85%');
            boardDiv.css('height', '65%');
        } else {
            // This is a chessboard.js board. Adjust for 1:1 aspect ratio
            desiredBoardWidth = Math.min(desiredBoardWidth, desiredBoardHeight);
            boardDiv.css('width', '100%');
            boardDiv.css('height', '100%');
        }
        if (board !== undefined) {
            board.resize();
        }
    }

    function fireEngine() {
        engineRunning = true;
        updateStatus();
        var currentScore;
        var msg = "position fen " + game.fen();
        console.log("GUI: " + msg);
        engine.postMessage(msg);
        msg = 'go movetime ' + $('#moveTime').val();
        console.log("GUI: " + msg);
        engine.postMessage(msg);
        engine.onmessage = function(event) {
            var line = event.data;

            console.log("ENGINE: " + line);
            var best = parseBestMove(line);
            if (best !== undefined) {
                var move = game.move(best);
                moveList.push(move);
                if (currentScore !== undefined) {
                    if (scoreList.length > 0) {
                        scoreList.pop(); // remove the dummy score for the user's prior move
                        scoreList.push(currentScore); // Replace it with the engine's opinion
                    }
                    scoreList.push(currentScore); // engine's response
                } else {
                    scoreList.push(0); // not expected
                }
                cursor++;
                board.position(game.fen(), true);
                engineRunning = false;
                updateStatus();
            } else {
                // Before the move gets here, the engine emits info responses with scores
                var score = parseScore(line);
                if (score !== undefined) {
                    if (player === 'w') {
                        score = -score; // convert from engine's score to white's score
                    }
                    updateScoreGauge(score);
                    currentScore = score;
                }
            }
        };
    }

    function parseBestMove(line) {
        var match = line.match(/bestmove\s([a-h][1-8][a-h][1-8])(n|N|b|B|r|R|q|Q)?/);
        if (match) {
            var bestMove = match[1];
            var promotion = match[2];
            return {
                from: bestMove.substring(0, 2),
                to: bestMove.substring(2, 4),
                promotion: promotion
            }
        }
    }

    function parseScore(line) {
        var match = line.match(/score\scp\s(-?\d+)/);
        if (match) {
            return match[1];
        } else {
            if (line.match(/mate\s-?\d/)) {
                return 2500;
            }
        }
    }






    function updateStatus() {

        var status = '';

        var moveColor = 'White';
        if (game.turn() === 'b') {
            moveColor = 'Black';
        }

        if (game.game_over()) {

            if (game.in_checkmate()) {
                status = moveColor + ' checkmated.';
            } else if (game.in_stalemate()) {
                status = moveColor + " stalemated";
            } else if (game.insufficient_material()) {
                status = "Draw (insufficient material)."
            } else if (game.in_threefold_repetition()) {
                status = "Draw (threefold repetition)."
            } else if (game.in_draw()) {
                status = "Game over (fifty move rule)."
            }
            swal({
                title: "Game Over",
                text: status,
                type: 'info',
                showCancelButton: false,
                confirmButtonColor: "#DD6655",
                onConfirmButtonText: 'OK',
                closeOnConfirm: true
            });
            engineRunning = false;
        }

        // game still on
        else {
            if (player === 'w') {
                status = "Computer playing Black; ";
            } else {
                status = "Computer playing White; ";
            }
            status += moveColor + ' to move.';

            // check?
            if (game.in_check() === true) {
                status += ' ' + moveColor + ' is in check.';
            }
        }

        fenEl.html(game.fen().replace(/ /g, '&nbsp;'));
        var currentPGN = game.pgn({
            max_width: 10,
            newline_char: "<br>"
        });
        var matches = entirePGN.lastIndexOf(currentPGN, 0) === 0;
        if (matches) {
            currentPGN += "<span>" + entirePGN.substring(currentPGN.length, entirePGN.length) + "</span>";
        } else {
            entirePGN = currentPGN;
        }
        pgnEl.html(currentPGN);
        if (engineRunning) {
            // status += ' Thinking...';
            status += ' ';
        }
        pgnEll.html(currentPGN);
        if (engineRunning) {
            // status += ' Thinking...';
            status += ' ';
        }
        statusEl.html(status);
    };

    // Set up chessboard
    var onDrop = function(source, target) {

        if (engineRunning) {
            return 'snapback';
        }

        if (board.hasOwnProperty('removeGreySquares') && typeof board.removeGreySquares === 'function') {
            board.removeGreySquares();
        }

        // see if the move is legal
        var move = game.move({
            from: source,
            to: target,
            promotion: 'q' //$("#promotion").val()
        });



        // illegal move
        if (move === null) return 'snapback';
        // highlight black's move

        removeHighlights('white')
        $board.find('.square-' + source).addClass('highlight-white')
        $board.find('.square-' + target).addClass('highlight-white')

        if (cursor === 0) {
            console.log("GUI: ucinewgame");
            engine.postMessage("ucinewgame");
        }
        moveList = moveList.slice(0, cursor);
        scoreList = scoreList.slice(0, cursor);
        moveList.push(move);
        // User just made a move- add a dummy score for now. We will correct this element once we hear from the engine
        scoreList.push(scoreList.length === 0 ? 0 : scoreList[scoreList.length - 1]);
        cursor = moveList.length;
    };
    var $board = $('#board')
    var squareClass = 'square-55d63'

    function removeHighlights(color) {
        $board.find('.' + squareClass)
            .removeClass('highlight-' + color)
    }
    // update the board position after the piece snap
    // for castling, en passant, pawn promotion
    var onSnapEnd = function() {

        if (!game.game_over() && game.turn() !== player) {
            fireEngine();
        }

    };

    var squareToHighlight = null

    function onMouseoverSquare(square, piece) {
        // get list of possible moves for this square
        var moves = game.moves({
            square: square,
            verbose: true
        })

        // exit if there are no moves available for this square
        if (moves.length === 0) {
            ondragpostion(square);
        }

        // highlight the square they moused over
        greySquare(square)

        // highlight the possible squares for this piece
        for (var i = 0; i < moves.length; i++) {
            board.addArrowAnnotation(square, moves[i].to)
            greySquare(moves[i].to)
        }
    }



    function ondragpostion(square) {
        //board.addArrowAnnotation(square, "h5"); 
    }

    function onMouseoutSquare(square, piece) {
        board.clearAnnotation()
        removeGreySquares()
    }

    function removeGreySquares() {
        $('#board .square-55d63').css('background', '')
    }

    function greySquare(square) {
        // alert(square);
        var square = $('#board .square-' + square)

        var background = whiteSquareGrey
        if (square.hasClass('black-3c85d')) {
            background = blackSquareGrey
        }

        square.css('background', background)


    }



    function onMoveEnd() {
        $board.find('.square-' + squareToHighlight)
            .addClass('highlight-black')
    }

    function createBoard(pieceSet, args, args1, args2) {
        // alert(pieceSet+"->"+args);
        var cfg = {

            cameraControls: true,
            draggable: true,
            position: 'start',
            onDrop: onDrop,
            onMouseoutSquare: onMouseoutSquare,
            onMouseoverSquare: onMouseoverSquare,
            onSnapEnd: onSnapEnd,
            onMoveEnd: onMoveEnd
                //overlay: true
        };

        // if (board3D) {
        //     if (pieceSet) {
        //         if (pieceSet === 'minions') {
        //             cfg.whitePieceColor = 0xFFFF00;
        //             cfg.blackPieceColor = 0xCC00CC;
        //             cfg.lightSquareColor = 0x888888;
        //             cfg.darkSquareColor = 0x666666;
        //         }
        //         cfg.pieceSet = '/static/assets/chesspieces/' + pieceSet + '/{piece}.json';
        //     }
        //     return new ChessBoard3('board', cfg);
        //   } else {
        if (args == '2D') {
            if (args1 == 'piece') {
                var selectedVal = $("#board-style option:selected").val();
                if (selectedVal == 'aluminium') {

                    // cfg.boardTheme = ["#6fadd4", "#d0ceca"];

                    return new ChessBoard('board', {
                        pieceTheme: '/static/img/chesspieces/' + pieceSet + '/{piece}.png',
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/ab.png')", "url('/static/img/chesspieces/board/aw.png')", "url('/static/img/chesspieces/board/ab.png')"]

                    });
                }
                if (selectedVal == 'cherry') {

                    //cfg.boardTheme = ["#521b01", "#b45119"];
                    return new ChessBoard('board', {
                        pieceTheme: '/static/img/chesspieces/' + pieceSet + '/{piece}.png',
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/cherry1.png')", "url('/static/img/chesspieces/board/cherry2.png')", "url('/static/img/chesspieces/board/cherry2.png')"]

                    });
                }
                if (selectedVal == 'lapis') {

                    //cfg.boardTheme = ["#244251", "#c9b46b"];
                    return new ChessBoard('board', {
                        pieceTheme: '/static/img/chesspieces/' + pieceSet + '/{piece}.png',
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/wb.png')", "url('/static/img/chesspieces/board/ww.png')", "url('/static/img/chesspieces/board/wb.png')"]

                    });
                }
                if (selectedVal == 'marble') {

                    //cfg.boardTheme = ["#bb886e", "#e9d2b7"];
                    return new ChessBoard('board', {
                        pieceTheme: '/static/img/chesspieces/' + pieceSet + '/{piece}.png',
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/marble1.png')", "url('/static/img/chesspieces/board/marble2.png')", "url('/static/img/chesspieces/board/marble1.png')"]

                    });
                }
                if (selectedVal == 'sand') {

                    //cfg.boardTheme = ["#c8a97d", "#fdedb7"];
                    return new ChessBoard('board', {
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/sand1.png')", "url('/static/img/chesspieces/board/sand2.png')", "url('/static/img/chesspieces/board/sand1.png')"],
                        pieceTheme: '/static/img/chesspieces/' + pieceSet + '/{piece}.png'
                    });
                }
                if (selectedVal == 'slate') {

                    //cfg.boardTheme = ["#8c8c8c", "#c9c9c9"];
                    return new ChessBoard('board', {
                        pieceTheme: '/static/img/chesspieces/' + pieceSet + '/{piece}.png',
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/slate1.png')", "url('/static/img/chesspieces/board/slate2.png')", "url('/static/img/chesspieces/board/slate2.png')"]

                    });
                } else {
                    //cfg.boardTheme = ["#ae6c37", "#d4b171"];#244251", "#c9b46b

                    return new ChessBoard('board', {
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/lapis/lapis1.png')", "url('/static/img/chesspieces/board/lapis/lapis2.png')", "url('/static/img/chesspieces/board/lapis/lapis2.png')"]


                    });

                }



                //cfg.pieceTheme = '/static/img/chesspieces/' + pieceSet + '/{piece}.png';


                //return new ChessBoard('board', cfg);
            }
            if (args1 == 'board') {
                if (pieceSet == 'aluminium') {
                    // cfg.boardTheme = ["#6fadd4", "#d0ceca"];
                    return new ChessBoard('board', {
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/ab.png')", "url('/static/img/chesspieces/board/aw.png')", "url('/static/img/chesspieces/board/ab.png')"]

                    });
                }
                if (pieceSet == 'cherry') {

                    //cfg.boardTheme = ["#521b01", "#b45119"];
                    return new ChessBoard('board', {
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/cherry1.png')", "url('/static/img/chesspieces/board/cherry2.png')", "url('/static/img/chesspieces/board/cherry2.png')"]

                    });
                }
                if (pieceSet == 'lapis') {

                    //cfg.boardTheme = ["#244251", "#c9b46b"];
                    return new ChessBoard('board', {
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/wb.png')", "url('/static/img/chesspieces/board/ww.png')", "url('/static/img/chesspieces/board/wb.png')"]

                    });
                }
                if (pieceSet == 'marble') {

                    //cfg.boardTheme = ["#bb886e", "#e9d2b7"];
                    return new ChessBoard('board', {
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/marble1.png')", "url('/static/img/chesspieces/board/marble2.png')", "url('/static/img/chesspieces/board/marble1.png')"]

                    });
                }
                if (pieceSet == 'sand') {

                    //cfg.boardTheme = ["#c8a97d", "#fdedb7"];
                    return new ChessBoard('board', {
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/sand1.png')", "url('/static/img/chesspieces/board/sand2.png')", "url('/static/img/chesspieces/board/sand1.png')"]

                    });
                }
                if (pieceSet == 'slate') {

                    //cfg.boardTheme = ["#8c8c8c", "#c9c9c9"];
                    return new ChessBoard('board', {
                        draggable: true,
                        position: 'start',
                        onDrop: onDrop,
                        onSnapEnd: onSnapEnd,
                        boardTheme: ["url('/static/img/chesspieces/board/slate1.png')", "url('/static/img/chesspieces/board/slate2.png')", "url('/static/img/chesspieces/board/slate2.png')"]

                    });
                }
                return new ChessBoard('board', cfg);
            }

        } else {
            //cfg.boardTheme = ["#ae6c37", "#d4b171"];#244251", "#c9b46b

            return new ChessBoard('board', {
                draggable: true,
                position: 'start',
                onDrop: onDrop,
                onSnapEnd: onSnapEnd,
                boardTheme: ["url('/static/img/chesspieces/board/lapis/lapis1.png')", "url('/static/img/chesspieces/board/lapis/lapis2.png')", "url('/static/img/chesspieces/board/lapis/lapis2.png')"]


            });

        }
    }



    adjustBoardWidth();
    board = createBoard();

    $(window).resize(function() {
        adjustBoardWidth();
    });

    // Set up buttons
    $('#startBtn').on('click', function() {
        var cursorStart = 0;
        if (player === 'b') {
            cursorStart = 1;
        }
        while (cursor > cursorStart) {
            game.undo();
            cursor--;
        }
        updateScoreGauge(0);
        board.position(game.fen());
        updateStatus();
    });
    $('#backBtn').on('click', function() {
        if (cursor > 0) {
            cursor--;
            game.undo();
            board.position(game.fen());
            var score = cursor === 0 ? 0 : scoreList[cursor - 1];
            updateScoreGauge(score);
            updateStatus();
        }
    });
    $('#forwardBtn').on('click', function() {
        if (cursor < moveList.length) {
            game.move(moveList[cursor]);
            var score = scoreList[cursor];
            updateScoreGauge(score);
            board.position(game.fen());
            cursor++;
            updateStatus();
        }
    });
    var pause_value = "play";
    $('#playBtn').on('click', function() {
        pause_value = "play";
        if (pause_value == "play") {
            play();
        } else {
            if (pause_value == "pause") {
                stop();
            } else {
                return;
            }
        }

    });

    function play() {
        var k = moveList.length;
        document.getElementById('movecount').value = k;
        // var pause = document.getElementById('playcount').value;
        var me = this;
        var delay = 1000;
        var timerId = null;
        var moveId = 0;
        for (i = k; i > 0; i--) {
            document.getElementById('movecount').value = i;
            setTimeout(function timer() {
                if (pause_value == 'pause') {

                } else {

                    game.move(moveList[cursor]);
                    var score = scoreList[cursor];
                    board.position(game.fen());
                    cursor++;
                    updateStatus();
                    updateScoreGauge(score);
                }

            }, i * delay);

        }
    }
    $('#pause').on('click', function() {
        pause_value = "pause";
        document.getElementById("board").disabled = true;
        if (pause_value == "play") {
            play();
        } else {
            //pause_value="play";
        }

    });

    function stop() {}
    $('#endBtn').on('click', function() {
        while (cursor < moveList.length) {
            game.move(moveList[cursor++]);
        }
        board.position(game.fen());
        updateScoreGauge(scoreList.length == 0 ? 0 : scoreList[cursor - 1]);
        updateStatus();
    });
    $('#hintBtn').on('click', function() {
        if (game.turn() === player) {
            engineRunning = true;
            var msg = "position fen " + game.fen();
            console.log("GUI: " + msg);
            engine.postMessage(msg);
            msg = 'go movetime ' + $('#moveTime').val();
            console.log(msg);
            engine.postMessage(msg);
            engine.onmessage = function(event) {
                console.log("ENGINE: " + event.data);
                var best = parseBestMove(event.data);
                if (best !== undefined) {
                    var currentFEN = game.fen();
                    game.move(best);
                    var hintedFEN = game.fen();
                    game.undo();
                    board.position(hintedFEN, true);
                    // give them a second to look before sliding the piece back
                    setTimeout(function() {
                        board.position(currentFEN, true);
                        engineRunning = false;
                    }, 1000); // give them a second to look
                }
            }
        }
    });
    $('#flipBtn').on('click', function() {
        if (game.game_over()) {
            return;
        }
        board.flip(); //wheeee!
        if (player === 'w') {
            player = 'b';
        } else {
            player = 'w';
        }
        updateStatus();
        setTimeout(fireEngine, 1000);
    });

    $('#dimensionBtn').on('click', function() {
        var dimBtn = $("#dimensionBtn");
        var sel = document.getElementById('dimensionBtn').value;
        dimBtn.prop('disabled', true);
        var position = board.position();
        var orientation = board.orientation();
        board.destroy();
        board3D = !board3D;
        adjustBoardWidth();
        if (sel == '3D') {

            dimBtn.val(board3D ? '3D' : '2D');
            setTimeout(function() {

                board = createBoard($('#piecesMenu').val(), sel);
                board.orientation(orientation);
                board.position(position);
                $("#dimensionBtn").prop('disabled', false);
            });
        }
        if (sel == '2D') {
            setTimeout(function() {

                board = createBoard($('#piece-style').val(), sel);
                console.log(board);
                board.orientation(orientation);
                board.position(position);
                $("#dimensionBtn").prop('disabled', false);

            });
        }


    });


    $("#setFEN").on('click', function(e) {
        swal({
            title: "SET FEN",
            text: "Enter a FEN position below:",
            type: "input",
            inputType: "text",
            showCancelButton: true,
            closeOnConfirm: false
        }, function(fen) {
            if (fen === false) {
                return; //cancel
            }
            fen = fen.trim();
            console.log(fen);
            var fenCheck = game.validate_fen(fen);
            console.log("valid: " + fenCheck.valid);
            if (fenCheck.valid) {
                game = new Chess(fen);
                console.log("GUI: ucinewgame");
                engine.postMessage('ucinewgame');
                console.log("GUI: position fen " + fen);
                engine.postMessage('position fen ' + fen);
                board.position(fen);
                fenEl.val(fen);
                pgnEl.empty();
                pgnEll.empty();
                updateStatus();
                swal("Success", "FEN parsed successfully.", "success");
            } else {
                console.log(fenCheck.error);
                swal.showInputError("ERROR: " + fenCheck.error);
                return false;
            }
        });
    });

    $("#setPGN").on('click', (function(e) {
        swal({
            title: "SET PGN",
            text: "Enter a game PGN below:",
            type: "input",

            showCancelButton: true,
            closeOnConfirm: false
        }, function(pgn) {
            if (pgn === false) {
                return; // cancel
            }
            pgn = pgn.trim();
            console.log(pgn);
            var pgnGame = new Chess();
            if (pgnGame.load_pgn(pgn)) {
                game = pgnGame;
                var fen = game.fen();
                console.log("GUI: ucinewgame");
                engine.postMessage('ucinewgame');
                console.log("GUI: position fen " + fen);
                engine.postMessage('position fen ' + game.fen());
                board.position(fen, false);
                fenEl.val(game.fen());
                pgnEl.empty();
                pgnEll.empty();
                moveList = game.history();
                scoreList = [];
                for (var i = 0; i < moveList.length; i++) {
                    scoreList.push(0);
                }
                cursor = moveList.length;
                updateStatus();
                swal("Success", "PGN parsed successfully.", "success");
            } else {
                swal.showInputError("PGN not valid.");
                return false;
            }
        });
    }));

    $("#resetBtn").on('click', function(e) {
        player = 'w';
        game = new Chess();
        fenEl.empty();
        pgnEl.empty();
        pgnEll.empty();
        largestPGN = '';
        moveList = [];
        scoreList = [];
        cursor = 0;
        board.start();
        board.orientation('white');
        console.log("GUI: ucinewgame");
        engine.postMessage('ucinewgame');
        updateScoreGauge(0);
    });

    $("#engineMenu").change(function() {
        console.log($("#engineMenu").val());
        if (engine) {
            var jsURL = $("#engineMenu").val();
            engine.terminate();
            engine = new Worker(jsURL);
            console.log("GUI: uci");
            engine.postMessage('uci');
            console.log("GUI: ucinewgame");
            engine.postMessage('ucinewgame');
            updateScoreGauge(0); // they each act a little differently
            if (jsURL.match(/p4wn/)) {
                swal('Using the tiny p4wn engine, which plays at an amateur level.');
            } else if (jsURL.match(/lozza/)) {
                swal('Using Lozza engine by Colin Jerkins, estimated rating 2340.')
            } else if (jsURL.match(/stockfish/)) {
                swal("Using stockfish engine, estimated rating > 3000.");
            }
        }
    });

    $('#piecesMenu').change(function() {
        var fen = board.position();
        board.destroy();
        board = createBoard($('#piecesMenu').val(), '3D', '');
        board.position(fen);
        adjustBoardWidth();
    });

    $('#piece-style').change(function() {
        var fen = board.position();
        board.destroy();
        board = createBoard($('#piece-style').val(), '2D', 'piece');
        board.position(fen);
        adjustBoardWidth();
    });
    $('#board-style').change(function() {
        var fen = board.position();
        board.destroy();
        board = createBoard($('#board-style').val(), '2D', 'board');
        board.position(fen);
        adjustBoardWidth();
    });

    updateStatus();
    //document.getElementById("pgn1").innerText = event.target.result;
    document.getElementById("pgn").innerText = event.target.result;
    pgn = event.target.result;
    var board;
    fenEl = $('#fen');



    pgn = pgn.trim();
    console.log(pgn);
    var pgnGame = new Chess();
    if (pgnGame.load_pgn(pgn)) {
        game = pgnGame;
        var fen = game.fen();
        console.log("GUI: ucinewgame");
        engine.postMessage('ucinewgame');
        console.log("GUI: position fen " + fen);
        engine.postMessage('position fen ' + game.fen());
        board.position(game.fen());
        fenEl.val(game.fen());
        pgnEl.empty();
        pgnEll.empty();
        moveList = game.history();
        scoreList = [];
        for (var i = 0; i < moveList.length; i++) {
            scoreList.push(0);
        }
        cursor = moveList.length;

        swal("Success", "PGN parsed successfully.", "success");
    } else {
        swal.showInputError("PGN not valid.");
        return false;
    }



}

function hideplay() {
    $('#playBtn').hide();
    $('#pause').css('display', 'initial');
    document.getElementById('playcount').value = 0;

}

function showplay() {
    $('#pause').css('display', 'none');
    $('#playBtn').show();

    document.getElementById('playcount').value = 1;
}

function download(file, text) {

    //creating an invisible element 
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8, ' +
        encodeURIComponent(text));
    element.setAttribute('download', file);

    //the above code is equivalent to 
    // <a href="path of file" download="file name"> 

    document.body.appendChild(element);

    //onClick property 
    element.click();

    document.body.removeChild(element);
}

// Start file download. 
document.getElementById("export").addEventListener("click", function() {
    // Generate download of hello.txt file with some content 
    var text = document.getElementById("pgn").innerText;
    var filename = "chessmove.pgn";

    download(filename, text);
}, false);