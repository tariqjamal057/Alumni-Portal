// Add mentor help post 
$(document).on("submit", "#create_mentor_help_post", function (e) {
    $("#add_help_desk_post").modal("hide");
  
    e.preventDefault();
    const mentor_help_post = new FormData($("#create_mentor_help_post")[0]);
    alert("working")
    $.ajax({
      type: "POST",
      url: "/request/create-mentor-help-post/",
      data: mentor_help_post,
      processData: false,
      contentType: false,
      success: function (response) {
        $("#mentor_help_post_container").html(response.html);
        swal({
          title: "Mentor help post",
          text: "Post Added Successfully",
          icon: "success",
          closeOnClickOutside: false,
          buttons: {
            cancel: {
              text: "Cancel",
              value: false,
              visible: true,
              closeModal: true,
            },
            confirm: {
              text: "ok",
              value: true,
              visible: true,
              closeModal: true,
            },
          },
        });
      },
    });
  });


// Delete a Post
function delete_mentor_help_post(id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajax({
    type: "POST",
    url: "/request/delete-mentor-help-post/",
    data: { id: id, csrfmiddlewaretoken: csrftoken },
    success: function (response) {
      var x = "#delete_mentor_help_post" + response["id"];
      $(x).modal("hide");
      if (response["success"] === true) {
        swal("success", "Mentor Help Post Deleted Successfully", "success");
        $("#mentor_help_post_container").html(response.html);
      }
    },
    error: function () {
      alert("No Data Found to delete");
    },
  });
}
