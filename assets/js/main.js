class Game{
    constructor(){
        this.link = "http://localhost:8080/";
        $(".image-user").on("click",this.changeAvatar);
        $("#btn-create-new").on("click", this.createGame);
        $("#btn-fold").on("click", this.foldGame);
        this.idGame = 0;
        this.playerId = 1;
        this.setInterval = null
    }
    sendCreateGame = async function(){
        let result = null;
        try {
            await $.ajax({
                url: game.link + "api/game/creategame/"+game.idGame,
                method: "GET",
                accepts: "application/json",
                contentType: "application/json",
                dataType: "json",
                error: function(jqXHR,textStatus,errorThrown ){

                },
                success: function (data) {
                    result = data
                }
            });
            return result;
        } catch (error) {
            return null;
        }
    }

    createGame = async function (event) {
        if(game.setInterval != null){
            clearInterval(game.setInterval)
        }
        let data = await game.sendCreateGame();
        if(data == null){
            event.stopPropagation();
            return;
        }
        game.idGame = data.idGame;
        let nrow = data.row;
        let ncol = data.col;
        $(".tablexo").html("");
        let table = "";
        for(let i = 0;i < nrow;i++){
            let row = '<div class="row">';
            $(".tablexo").append(row);
            for(let j = 0;j<ncol;j++){
                let id = i * ncol + j;
                let col = '<div class="col" id="'+id+'"></div>';
                row += col;
            }
            row += "</div>";
            table += row;
        }
        $(".tablexo").html(table);
        game.addEventPlay();
        alert("Start game!");
        event.stopPropagation();
    }

    addEventPlay = function () {
        $(".col").on("click", game.playGame);
    }

    sendPlayGame = async function (id) {
        let result = null;
        try {
            await $.ajax({
                url: game.link + "api/game/playgame/"+game.idGame+"/"+id,
                method: "GET",
                accepts: "application/json",
                contentType: "application/json",
                dataType: "json",
                error: function(jqXHR,textStatus,errorThrown ){

                },
                success: function (data) {
                    result = data
                }
            });
            return result;
        } catch (error) {
            return null;
        }
    }

    playGame = async function(event){
        let id = $(event.target).attr("id");
        let data = await game.sendPlayGame(id);
        if(data == null){
            event.stopPropagation();
            return;
        }
        if(data.player1 != null){
            game.executeDataPlayer(data.player1);
        }
        if(data.player2 != null){
            game.executeDataPlayer(data.player2)
        }
        event.stopPropagation();
    }

    executeDataPlayer = function (data) {
        let playerId = data.playerId;
        let mark = data.mark;
        let action = data.action;
        let gameOver = data.win;
        let arrayWin = data.array;
        if(mark == -1){
            return;
        }
        if(mark == 1){
            $("#"+action).addClass("x");
        }else{
            $("#"+action).addClass("o");
        }
        if(gameOver){
            if(playerId == game.playerId){
                alert("You win!");
            }else{
                alert("You lost!");
            }
            game.executeWinGame(arrayWin);
        }
    }

    executeWinGame = function(arrayWin){
        arrayWin.forEach(m => {
            $("#"+m).addClass("col-win win");
        });
        game.setInterval = setInterval(() => {
            if($(".win").hasClass("col-win")){
                $(".win").removeClass("col-win");
            }else{
                $(".win").addClass("col-win");
            }
        }, 500);
    }

    sendFoldGame = async function(){
        try {
            let result = null;
            await $.ajax({
                url: game.link + "api/game/foldgame/"+game.idGame,
                method: "GET",
                accepts: "application/json",
                contentType: "application/json",
                dataType: "json",
                error: function(jqXHR,textStatus,errorThrown ){

                },
                success: function (data) {
                    result = data
                }
            });
            return result;
        } catch (error) {
            return null;
        }
    }

    foldGame = async function(event){
        let data = await game.sendFoldGame();
        if(data == null){
            event.stopPropagation();
            return;
        }
        alert(data.message);
        event.stopPropagation();
    }

    changeAvatar = function(event){
        parent = $(event.target).parent()
        if($(parent).hasClass("user")){
            if($(event.target).hasClass("image-nam")){
                $(event.target).removeClass("image-nam");
                $(event.target).addClass("image-nu");
            }else{
                $(event.target).removeClass("image-nu");
                $(event.target).addClass("image-nam");
            }
        }else{
            if($(event.target).hasClass("image-bot1")){
                $(event.target).removeClass("image-bot1");
                $(event.target).addClass("image-bot2");
            }else{
                $(event.target).removeClass("image-bot2");
                $(event.target).addClass("image-bot1");
            }
        }
        event.stopPropagation();
    }
}

$(document).ready(function () {
    game = new Game();
})