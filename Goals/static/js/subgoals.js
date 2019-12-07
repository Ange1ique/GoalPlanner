$(function () {

  /* Responsive buttons and forms */

  var responsive = function mobileViewUpdate() {
    var viewportWidth = $(window).width();
    if (viewportWidth < 600) {
      $(".btn").addClass("btn-sm");
      $(".form-control").addClass("form-control-sm");
      $(".input-group").addClass("input-group-sm");
    }
    else {
      $(".btn").removeClass("btn-sm");
      $(".checkbutton").addClass("btn-sm");
      $(".form-control").removeClass("form-control-sm");
      $(".input-group").removeClass("input-group-sm");
    }
  };

  $(window).on('resize', responsive).resize();

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("href"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-subgoal").modal("show");
      },
      success: function (data) {
        $("#modal-subgoal .modal-content").html(data.html_form);
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
          $("#modal-subgoal").modal("hide");
          $('#listofsubgoals').load(' #listofsubgoals > *', function(){
            responsive()});
        }
      }
    });
    return false;
  };

  /* Binding */

  // Delete subgoal
  $("#listofsubgoals").on("click", ".js-delete-subgoal", loadForm);
  $("#modal-subgoal").on("submit", ".js-subgoal-delete-form", saveForm);

  // Delete activity
  $("#listofsubgoals").on("click", ".js-delete-activity", loadForm);
  $("#modal-subgoal").on("submit", ".js-activity-delete-form", saveForm);

  /* Save form or add activity */

  $(document).on('click', '.js-save-goal', function(event){
    event.preventDefault();
    var saveButton = $(this).attr('id');
    var editSubgoalsForm = $('#editsubgoalsform');
    var data = editSubgoalsForm.serialize();
    $.ajax({
      url: '',
      data: data,
      type: 'post',
      dataType: 'json',
      success: function (data) {
        if (data == 'success') {
          $('#listofsubgoals').load(' #listofsubgoals > *', function(){
            if (saveButton == 'save_goal'){
              $("#modal-save-goal").modal("show")
            }
            responsive()
          });
        }
        else {
          $("#modal-error-goal").modal("show")
        }
      },
      error: function(){
        console.log("Unknown error?");
      },
    })
    return false;
  });

});
