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
          delayed_img_update();
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