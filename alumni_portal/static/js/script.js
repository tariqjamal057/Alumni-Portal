// Help desk post section

function addchat(id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  const message = document.getElementById("alumni_msg" + id).value;
  console.log("message = " + message);
  $.ajax({
    type: "POST",
    url: "/user_response/",
    data: { message: message, id: id, csrfmiddlewaretoken: csrftoken },
    success: function (response) {
      $("#help_desk_post_message").html(response.html);
    },
    error: () => {
      console.log("Something went wrong in ");
    },
  });
}

function get_helpdesk_post_id(id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajax({
    type: "POST",
    url: "/get_user_message/",
    data: { id: id },
    success: function (response) {
      $("#help_desk_post_message").html(response.html);
    },
    error: () => {
      console.log("Something went wrong in help ");
    },
  });
}
