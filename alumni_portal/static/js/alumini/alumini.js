function alumni_addchat(id) {
    const csrftoken = $("[name=csrfmiddlewaretoken]").val();
    alert(id);
    const message = document.getElementById("alumni_msg"+id).value;
    alert(message)
    console.log("message = " + message);
    $.ajax({
      type: "POST",
      url: "/alumni_response/",
      data: { message: message, id: id, csrfmiddlewaretoken: csrftoken },
      success: function (response) {
          alert("yes")
        var x = "#chat" + response["id"];
        $(x).modal("hide");
        $("#finance_request_container").html(response.html);
      },
      error: () => {
        alert("Something went wrong");
      },
    });
  }