// Updates the icon every 1000 ms
$(document).ready(setInterval(function() {
  $.ajax({
    url: '/media/update_buttons',
    type: 'get',
    contentType: 'application/json',
    success: function(response) {
      $('.videostatus-icon').text(response.icon)
      $('.videostatus-class').removeClass("red").removeClass("green").removeClass("blue").addClass(response.theclass)
    }
  })
}, 1000));


// Updates the icon on click
$(document).ready(function () {
  $('.update-btn-videos').click(function(){
    $.ajax({
      url: '/media/update_buttons',
      type: 'get',
      contentType: 'application/json',
      success: function(response) {
        $('.videostatus-icon').text(response.icon)
        $('.videostatus-class').removeClass("red").removeClass("green").removeClass("blue").addClass(response.theclass)
      }
    })
  })
});


// Submits video to flask
$(document).ready(function () {
  $('.submit-btn-videos').click(function(){
    $.ajax({
      url: '/media/submit_video',
      type: 'post',
      contentType: 'application/json',
      data: JSON.stringify ($('.video-input-field').val()),
      success: function(response) {
      console.log($('.video-input-field').val()); 
      }
    })
  })
});

// Submits image to flask
$(document).ready(function () {
  $('.submit-btn-files').click(function(){
    var form_data = new FormData();
    form_data.append('file', $('#file-upload').prop('files')[0]);
    $.ajax({
      type: 'POST',
      url: '/media/submit_file',
      data: form_data,
      contentType: false,
      cache: false,
      processData: false,
      success: function(data) {
      console.log(form_data);
      }
    })
  })
});