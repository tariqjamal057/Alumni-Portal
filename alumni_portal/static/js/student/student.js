// Delete MentorHelp Post
function delete_post(id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajax({
    type: "POST",
    url: "/request/delete_mentor_help_post/",
    data: { id: id, csrfmiddlewaretoken: csrftoken },
    success: function (response) {
      var x = "#deletePost" + response["id"];
      $(x).modal("hide");
      if (response["success"] === true) {
        swal("success", "Post Deleted Successfully", "success");
        $("#post_container").html(response.html);
      }
    },
    error: function () {
      alert("No Post Found to delete");
    },
  });
}



