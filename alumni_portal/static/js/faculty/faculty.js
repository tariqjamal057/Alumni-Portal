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
  alert(id);
  const message = document.getElementById("alumni_msg" + id).value;
  alert(message);
  console.log("message = " + message);
  $.ajax({
    type: "POST",
    url: "/get_interest/",
    data: { 'message': message, 'id': id, 'csrfmiddlewaretoken': csrftoken,'chatfun':true},
    success: function (response) {
      alert("yes");
      var x = "#chat" + response["id"];
      $(x).modal("hide");
      $("#finance_request_container").html(response.html);
      alert(response);
    },
    error: () => {
      alert("Something went wrong");
    },
  });
}

// Get Interest Shown Alumni 
function get_interest_message(post,user) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajax({
    type: "POST",
    url: "/get_interest/",
    data: {'post_id':post,'user' :user},
    success: function (response) {
      $("#msg_container").html(response.html);
    },
    error: () => {
      alert("Something went wrong")
    },
  });
}

// Add amount for a Particular Finance post
function add_amount(post,user) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajax({
    type: "POST",
    url: '/add_amount/',
    data: {'post_id':post,'user' :user,},
    success: (response) => {
      $("#sponser").html(response.html);
      console.log("post interest recieved")
    },
    error: ()=> {
      alert("Something went wrong")
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
    data: {'studentname':studentname,'alumniname':alumniname,'amount':amount,'postid':postid,"alumniid":alumniid},
    success: (response) => {
      $('$#addamount').modal("hide")
      alert("Sponser Added")
    },
    error: ()=> {
      alert("Something went wrong")
    },
  });
}