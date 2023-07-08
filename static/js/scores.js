$(document).ready(function () {
    $('.update-btn-ctrscores').click(function(){
      $.ajax({
        url: '/ctrscores/update_scores',
        type: 'get',
        contentType: 'application/json',
        success: function(response) {
          $('.score-update-p1').text(response.scores.p1[0])
          $('.score-update-p2').text(response.scores.p2[0])
          $('.score-update-p3').text(response.scores.p3[0])
          $('.score-update-p4').text(response.scores.p4[0])
        }
      })
    })
})

// Updates everything on screen every second
$(document).ready(setInterval(function() {
    $.ajax({
    url: '/ctrscores/update_scores',
    type: 'get',
    contentType: 'application/json',
    success: function(response) {
        $('.score-update-p1').text(response.scores.p1[0])
        $('.score-update-p2').text(response.scores.p2[0])
        $('.score-update-p3').text(response.scores.p3[0])
        $('.score-update-p4').text(response.scores.p4[0])
        $('.score-update-img').attr('src', '/static/output/banner_scores.png' + '?' + new Date().getTime())
      }
    })
  }, 1000));

// These functions make the buttons with icons work
$(document).ready(function () {
  $('.send-btn-ctrscores').click(function(){
    $.ajax({
      url: '/ctrscores/draw_banner',
      type: 'post',
      contentType: 'application/json',
      //data: JSON.stringify ($('.video-input-field').val()),
      success: function(response) {
      console.log("Drawing Scores"); 
      }
    })
  })
});

$(document).ready(function () {
  $('.delete-btn-ctrscores').click(function(){
    $.ajax({
      url: '/ctrscores/reset_scores',
      type: 'post',
      contentType: 'application/json',
      //data: JSON.stringify ($('.video-input-field').val()),
      success: function(response) {
      console.log("Resetting Scores"); 
      }
    })
  })
});

