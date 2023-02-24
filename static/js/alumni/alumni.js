//Finance Request section 
// Chat with Faculty in Alumni as sponser
function alumni_addchat(id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  const message = document.getElementById("alumni_msg").value;
  if(message != '') {
    $.ajax({
      type: "POST",
      url: "/alumni_response/",
      data: { message: message, id: id, csrfmiddlewaretoken: csrftoken},
      success: function (response) {
        $(".message_box").html(response.html);
        document.getElementById("alumni_msg").value = "";
        scroll_to_bottom();
      },
      error: () => {
        console.log("something went wrong");
      },
    });
  }
  else {
    alert("Enter Your Message")
  }
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




// Help Desk Section 

// Delete Help desk post 
function help_desk_post_delete(id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajax({
    type: "POST",
    url: "/delete-help-desk-post/",
    headers:{"X-CSRFToken": csrftoken},
    data: { 'id': id },
    success: function (response) {
      var x = "#deleteRequest" + response["id"];
      $(x).modal("hide");
      if (response["success"] === true) {
        swal("success", "Help Desk Post Deleted Successfully", "success");
        $("#finance_request_div").html(response.html);
      }  
    },  
    error: function () {
      alert("No Data Found to delete");
    },  
  });  
}  

// Get Interest Shown Alumni 
function get_message_header(post,user) {
    const csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $.ajax({
      type: "POST",
      url: "/get_help_desk_chat_header/",
      data: {'post_id':post,'user' :user,'csrfmiddlewaretoken': csrftoken},
      success: function (response) {
        $(".upper_container").html(response.html);
      },
      error: () => {
        console.log("Something went wrong in get interest")
      },
    });
}

function get_helpdesk_interest_message(post,user,interest_id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajax({
    type: "POST",
    url: "/help_desk_interest_message/",
    data: {'post_id':post,'user' :user,'interest_id':interest_id,'csrfmiddlewaretoken': csrftoken},
    success: function (response) {
      $(".message_container").html(response.html);
      $("#message_send_button").attr("onclick","alumni_addchat('"+response.interest_id+"')");
      scroll_to_bottom();
    },
    error: () => {
      console.log("Something went wrong in get message interest")
    },
  });
}

function alumni_addchat(id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  const message = document.getElementById("alumni_msg").value;
  if(message != '') {
    $.ajax({
      type: "POST",
      url: "/alumni_response/",
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

function alumni_post_search() {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  const query = $('#search_query').val()
  $.ajax({
    type: "POST",
    url: "/alumni_post_search/",
    headers:{"X-CSRFToken": csrftoken},
    data: { 'query': query },
    success: function (response) {
      $("#finance_request_div").html(response.html);
    },  
    error: function () {
      alert("Something went wrong");
    },  
  });  
}
