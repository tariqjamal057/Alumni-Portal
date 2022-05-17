function alumni_addchat(id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  alert(id);
  const message = document.getElementById("alumni_msg" + id).value;
  alert(message);
  console.log("message = " + message);
  $.ajax({
    type: "POST",
    url: "/alumni_response/",
    data: { message: message, id: id, csrfmiddlewaretoken: csrftoken},
    success: function (response) {
      alert("yes");
      var x = "#chat" + response["id"];
      $(x).modal("hide");
      $("#alumni_message").html(response.html);
      alert(response);
    },
    error: () => {
      alert("Something went wrong");
    },
  });
}

function get_post_id(id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajax({
    type: "POST",
    url: "/get_alumni_message/",
    data: { id: id},
    success: function (response) {
      $("#alumni_message").html(response.html);
    },
    error: () => {
      alert("Something went wrong");
    },
  });
}
