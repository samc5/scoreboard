// scoreboard.js

// This code will repeatedly make an AJAX request to the '/score' endpoint
// and update the scores on the page every 5 seconds.

// Define a function that will make the AJAX request and update the scores on the page
function updateScores() {
    $.ajax({
        url: '/scoreboard',
        dataType: 'json',
        success: function(data) {
            $('#home_score').text(data.home);
            $('#away_score').text(data.away);
            $('#count-element').text(`Count: ${data.balls}-${data.strikes}`);
            $('#outs-count').text(`Outs: ${data.outs}`);
            $('#inning-count').text(`${data.inning}`);
            $('#pitcher-info').text(`Pitcher: ${data.pitcher_last}`);
            $('#batter-info').text(`Batter: ${data.batter_last}`);
            $('#base_1').attr('fill', data.base_colors[2]);
            $('#base_2').attr('fill', data.base_colors[1]);
            $('#base_3').attr('fill', data.base_colors[0]);
            $('#base_1').attr('stroke', data.base_colors[2]);
            $('#base_2').attr('stroke', data.base_colors[1]);
            $('#base_3').attr('stroke', data.base_colors[0]);
        }
    });
}

// Call the updateScores() function every 5 seconds using setInterval()
setInterval(updateScores, 5000);