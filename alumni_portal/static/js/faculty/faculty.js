// Delete Financial Request Post
function delete_post(id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajax({
    type: "POST",
    url: "/delete-finance-post/",
    headers:{"X-CSRFToken": csrftoken},
    data: { 'id': id },
    success: function (response) {
      var x = "#deleteRequest" + response["id"];
      $(x).modal("hide");
      if (response["success"] === true) {
        swal("success", "Finance Request Deleted Successfully", "success");
        $("#finance_request_div").html(response.html);
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
  if(message != '') {
    $.ajax({
      type: "POST",
      url: "/faculty_chat/",
      data: { 'message': message, 'id': id, 'csrfmiddlewaretoken': csrftoken},
      success: function (response) {
        $(".message_container").html(response.html);
        document.getElementById("alumni_msg").value = "";
        scroll_to_bottom();
      },
      error: () => {
        comsole.log("Something went wrong in faculty chat");
      },
    });
  }
  else {
    alert("Enter Your Message")
  }
}

// Get Interest Shown Alumni 
function get_interest_message(post,user,interest_id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajax({
    type: "POST",
    url: "/get_finance_request_messages/",
    data: {'post_id':post,'user' :user,'interest_id':interest_id,'csrfmiddlewaretoken': csrftoken},
    success: function (response) {
      $(".message_container").html(response.html);
      $("#message_send_button").attr("onclick","faculty_addchat('"+response.interest_id+"')");
      scroll_to_bottom();
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
  if(amount > 0 && amount != '') {
    $.ajax({
      type: "POST",
      url: '/add_sponser/',
      data: {'studentname':studentname,'alumniname':alumniname,'amount':amount,'postid':postid,"alumniid":alumniid,
    "csrfmiddlewaretoken":csrftoken},
      success: (response) => {
        $('.sponser_modal').addClass('hide_modal')
        swal({
          title: "Amount Added",
          text: "Amount added for Student",
          icon: "success",
          button: "Done",
        });

        $('#addamount2').modal('toggle');
      },
      error: ()=> {
        console.log("Something went wrong")
      },
    });
  }
  else {
    alert("Enter Correct Amount");
  }
}


