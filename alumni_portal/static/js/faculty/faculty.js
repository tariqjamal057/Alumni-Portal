// Delete Financial Request Post
function delete_post(id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajax({
    type: "POST",
    url: "/request/delete-finance-post/",
    data: { id: id, csrfmiddlewaretoken: csrftoken },
    success: function (response) {
      var x = "#deleteRequest" + response["id"];
      $(x).modal("hide");
      if (response["success"] === true) {
        swal("success", "Finance Request Deleted Successfully", "success");
        $("#finance_request_container").html(response.html);
      }
    },
    error: function () {
      alert("No Data Found to delete");
    },
  });
}

// Chat with Alumni for Finance Request
function faculty_addchat(id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  const message = document.getElementById("alumni_msg").value;
  $.ajax({
    type: "POST",
    url: "/faculty_chat/",
    data: { 'message': message, 'id': id, 'csrfmiddlewaretoken': csrftoken},
    success: function (response) {
      $(".message_container").html(response.html);
    },
    error: () => {
      comsole.log("Something went wrong in faculty chat");
    },
  });
}

// Get Interest Shown Alumni 
function get_interest_message(post,user) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajax({
    type: "POST",
    url: "/get_finance_request_messages/",
    data: {'post_id':post,'user' :user,'csrfmiddlewaretoken': csrftoken},
    success: function (response) {
      $(".message_container").html(response.html);
    },
    error: () => {
      console.log("Something went wrong in get message interest")
    },
  });
}

function get_interest(post,user) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajax({
    type: "POST",
    url: "/get_interest/",
    data: {'post_id':post,'user' :user,'csrfmiddlewaretoken': csrftoken},
    success: function (response) {
      $(".upper_container").html(response.html);
    },
    error: () => {
      console.log("Something went wrong in get interest")
    },
  });
}
function get_text_area_interest(post,user) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajax({
    type: "POST",
    url: "/finance_response_interest/",
    data: {'post_id':post,'user' :user,'csrfmiddlewaretoken': csrftoken},
    success: function (response) {
      $(".text_area_container").html(response.html);
      console.log(response.html)
    },
    error: () => {
      comsole.log("Something went wrong in get_text_area_interest")
    },
  });
}

// Add amount for a Particular Finance post
function add_amount(post,user) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajax({
    type: "POST",
    url: '/add_amount/',
    data: {'post_id':post,'user' :user,'csrfmiddlewaretoken':csrftoken},
    success: (response) => {
      $("#sponser").html(response.html)
      console.log("post interest recieved")
    },
    error: ()=> {
      console.log("Something went wrong")
    },
  });
}

// Adding Alumni as a sponser for particular Finance Post 
function add_sponser(postid,alumniid) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  const studentname = document.getElementById('studentname').value; 
  const alumniname = document.getElementById('alumniname').value; 
  const amount = document.getElementById('amount').value; 
  $.ajax({
    type: "POST",
    url: '/add_sponser/',
    data: {'studentname':studentname,'alumniname':alumniname,'amount':amount,'postid':postid,"alumniid":alumniid,
  "csrfmiddlewaretoken":csrftoken},
    success: (response) => {
      $('#addamount').modal('hide');
      swal({
        title: "Amount Added",
        text: "Amount added for Student",
        icon: "success",
        button: "Done",
      });
    },
    error: ()=> {
      console.log("Something went wrong")
    },
  });
}