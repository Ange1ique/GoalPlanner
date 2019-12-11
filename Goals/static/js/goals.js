$(function () {

  /* Responsive buttons and margins */

  var responsive = function mobileViewUpdate() {
    var viewportWidth = $(window).width();
    if (viewportWidth < 768) {
      $(".btn").addClass("btn-sm");
      $(".list-group-item").addClass("m-0 px-2");
    }
    else {
      $(".btn").removeClass("btn-sm");
      $(".checkbutton").addClass("btn-sm");
      $(".list-group-item").removeClass("m-0 px-2");
    }
  };

  $(window).on('resize', responsive).resize();

  /* CSRF check */

  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = cookies[i].trim();
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }

  var csrftoken = getCookie('csrftoken');

  /* Activity Button */

  $(document).on('click', '.checkbutton', function(event){
    event.preventDefault();
    var goal_id = parseInt($(this).attr('data-goalid'));
    var subgoal_id = parseInt($(this).attr('data-subgoalid'));
    var pk = parseInt($(this).attr('data-checkid'));
    var progress = parseInt($(this).attr('data-checkprogress'));
    if (progress == 100){progress = 0}
    else {progress = 100}
    var data_send = {
      'activity_id': pk,
      'progress': progress
    };
    $.ajax({
      headers: { "X-CSRFToken": csrftoken },
      type: 'POST',
      url: '/goals/progress/',
      data: data_send,
      dataType: 'json',
      success: function(){
        $('#reloadgoal' + goal_id).load(' #reloadgoal' + goal_id + ' > *', function(){
          $('#collapse2' + subgoal_id).addClass('show');
          responsive();
        });
      },
      error: function(){
        console.log("nog verder debuggen")
      },
    });
  });

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-goal").modal("show");
      },
      success: function (data) {
        $("#modal-goal .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-goal").modal("hide");
          $('#listofgoals').load(' #listofgoals > *', function(){
            responsive()});
        }
        else {
          $("#modal-goal .modal-content").html(data.html_form, function(){
            responsive()});
        }
      }
    });
    return false;
  };

  /* Binding */

  // Create goal
  $(".js-create-goal").click(loadForm);
  $("#modal-goal").on("submit", ".js-goal-create-form", saveForm);

  // Update goal
  $("#listofgoals").on("click", ".js-update-goal", loadForm);
  $("#modal-goal").on("submit", ".js-goal-update-form", saveForm);

  // Delete goal
  $("#listofgoals").on("click", ".js-delete-goal", loadForm);
  $("#modal-goal").on("submit", ".js-goal-delete-form", saveForm);

});
