// // Add Finance request
// $(document).on("submit", "#create_request", function (e) {
//   e.preventDefault();
//   // alert('hai');
//   $("#addFinancialRequest").modal("hide");

//   const financial_request_form = new FormData($("#create_request")[0]);
//   $.ajax({
//     type: "POST",
//     url: "/request/create-finance-post/",
//     data: financial_request_form,
//     processData: false,
//     contentType: false,
//     success: function (response) {
//       $("#finance_request_container").html(response.html);
//       console.log("saved in database");
//       swal({
//         title: "Add Financial",
//         text: "Financial Request Added",
//         icon: "success",
//         closeOnClickOutside: false,
//         buttons: {
//           cancel: {
//             text: "Cancel",
//             value: false,
//             visible: true,
//             closeModal: true,
//           },
//           confirm: {
//             text: "ok",
//             value: true,
//             visible: true,
//             closeModal: true,
//           },
//         },
//       });
//     },
//   });
// });

// update Finance Request
function update_form(id) {
  alert(id);
  const financial_request_form = new FormData($("update_request")[0]);
  // alert(financial_request_form)
  $.ajax({
    type: "POST",
    url: "/request/update-finance-post/",
    data: { form: financial_request_form, id: id, type: "get" },
    processData: false,
    contentType: false,
    success: function (response) {
      var x = "#updateFinancialRequest" + response["id"];
      $(x).modal("hide");
      $("#finance_request_container").html(response.html);
      swal({
        title: "Update Financial Request",
        text: "Financial Request updated",
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
    error: () => {
      alert("Something went wrong");
    },
  });
}

// Delete a Post
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

// Add Chat Message to database

// function addchat(id){
//     // $('#addFinancialRequest').modal('hide');
//     const chat = ($('#message'+id).val());
//     if(chat != ""){
//         console.log(id)
//         console.log(chat)
//         $.ajax({
//             type : 'POST',
//             url : '/chat/',
//             data : {'chat':chat,'id':id},
//             success : function(response){
//                 $('#messagearea').html(response.html);
//             }
//         });
//     }
// };

function get_form(id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajax({
    type: "POST",
    url: "/request/update-finance-post/",
    data: id,
    success: function (response) {
      alert("Form id Get Successful " + id);
    },
  });
}

function addchat(id) {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  alert(id);
  const message = document.getElementById("chat_btn"+id).value;
  alert(message)
  console.log("message = " + message);
  $.ajax({
    type: "POST",
    url: "/chat/",
    data: { message: message, id: id, csrfmiddlewaretoken: csrftoken },
    success: function (response) {
      var x = "#chat" + response["id"];
      $(x).modal("hide");
      $("#finance_request_container").html(response.html);
    },
    error: () => {
      alert("Something went wrong");
    },
  });
}



// Load more pagination 
function load_more() {
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
    var _currentResult = $(".post-container").length;
    console.log("sjjcj");
    // Run Ajax
    $.ajax({
      url: "/load-more/",
      type: "post",
      data: {
        offset: _currentResult,
        csrfmiddlewaretoken: "{{csrf_token}}",
      },
      dataType: "json",
      beforeSend: function () {
        $("#loadmoreBtn").addClass("disabled").text("Loading..");
      },
      success: function (res) {
        var _html = "";
        var json_data = $.parseJSON(res.posts);
        $.each(json_data, function (index, data) {
          _html +=
          '<div style="display: flex" class="post-container">\
            <div class="img-square-wrapper" style="margin-right: 10px">\
              //<img style="width: 100px; height: 100px" class="" src="'+ data.fields.image +'"alt="Card image cap" />\
            </div>\
            <div style="flex: 1">\
              <h5>'+ data.fields.student_name +'</h5>\
              <p class="card-text">'+data.fields.title +'</p>\
              <p>₹ '+data.fields.amount +'.00</p>\
            </div>\
          </div>';
        });
        $(".post-wrapper").append(_html);
        var _countTotal = $(".post-container").length;
        if (_countTotal == res.totalResult) {
          $("#loadmoreBtn").remove();
        } else {
          $("#loadmoreBtn").removeClass("disabled").text("Load More");
        }
      },
    });
  }
