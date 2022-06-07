// Help Desk Section 

// Delete Help desk post 
function delete_post(id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajax({
    type: "POST",
    url: "/request/delete_help_desk_post/",
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

// function alumni_addchat(id) {
//   const csrftoken = $("[name=csrfmiddlewaretoken]").val();
//   alert(id);
//   const message = document.getElementById("alumni_msg" + id).value;
//   alert(message);
//   console.log("message = " + message);
//   $.ajax({
//     type: "POST",
//     url: "/get_user_interest/",
//     data: { 'message': message, 'id': id, 'csrfmiddlewaretoken': csrftoken,'chat':true},
//     success: function (response) {
//       alert("yes");
//       var x = "#chat" + response["id"];
//       $(x).modal("hide");
//       $("#finance_request_container").html(response.html);
//       alert(response);
//     },
//     error: () => {
//       alert("Something went wrong");
//     },
//   });
// }

// Get Interest Shown User 
function get_interest_message(post,user) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  alert("working")
  alert(post)
  alert(user)
  $.ajax({
    type: "POST",
    url: "/get_user_interest/",
    data: {'post_id':post,'user' :user},
    success: function (response) {
      $("#user_msg_container").html(response.html);
    },
    error: () => {
      alert("Something went wrong")
    },
  });
}



//Finance Request section 

// Chat with Faculty in Alumni as sponser
function alumni_addchat(id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  const message = document.getElementById("alumni_msg" + id).value;
  console.log("message = " + message);
  $.ajax({
    type: "POST",
    url: "/alumni_response/",
    data: { message: message, id: id, csrfmiddlewaretoken: csrftoken},
    success: function (response) {
      var x = "#chat" + response["id"];
      $(x).modal("hide");
      $("#alumni_message").html(response.html);
    },
    error: () => {
      console.log("something went wrong");
    },
  });
}

function get_post_id(id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajax({
    type: "POST",
    url: "/get_alumni_message/",
    data: { id: id,csrfmiddlewaretoken: csrftoken},
    success: function (response) {
      $("#alumni_message").html(response.html);
    },
    error: () => {
      console.log("something went wrong")
    },
  });
}


//Alumni as Mentor Section

// Chat with student as Alumni as mentor 
function addchat(id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  const message = document.getElementById("alumni_msg" + id).value;
  console.log("message = " + message);
  $.ajax({
    type: "POST",
    url: "/mentor_message/",
    data: { message: message, id: id, csrfmiddlewaretoken: csrftoken },
    success: function (response) {
      $("#mentor_help_post_message").html(response.html);
    },
    error: () => {
      console.log("Something went wrong in ");
    },
  });
}

function get_mentor_messages(id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajax({
    type: "POST",
    url: "/get_mentor_message/",
    data: { id: id },
    success: function (response) {
      $("#mentor_help_post_message").html(response.html);
    },
    error: () => {
      console.log("Something went wrong in help ");
    },
  });
}
