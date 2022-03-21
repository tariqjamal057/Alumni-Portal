// Add Finance request
$(document).on('submit','#create_request',function(e) {
    $('#addFinancialRequest').modal('hide');
    
    e.preventDefault();
    const financial_request_form = new FormData($('#create_request')[0]);
    $.ajax({
        type : 'POST',
        url : '/request/create-finance-post/',
        data : financial_request_form,
        processData:false,
        contentType:false,
        success : function(response){
            $('#finance_request_container').html(response.html);
            swal({
                title: "Add Financial",
                text: "Financial Request Added",
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
                        closeModal: true
                    }
                }
            });
        }
    });
});

// update Finance Request
function updateRequest(id,e) {
    e.preventDefault();
    const financial_request_form = new FormData($('update_request')[0]);
    $.ajax({
        type : 'POST',
        url : '/request/update-finance-post/',
        data : financial_request_form,
        processData:false,
        contentType:false,
        success : function(response){
            var updatemodal = "#updateFinancialRequest"+response["id"]
            $(updatemodal).modal('hide');
            $('#finance_request_container').html(response.html);
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
                        closeModal: true
                    }
                }
            });
        },
        error : ()=> {
            alert("Product was not updated")
        }
    });
}

// Delete a Post
function delete_post(id){
    const csrftoken = $('[name=csrfmiddlewaretoken]').val();
    $.ajax({
        type : 'POST',
        url : '/request/delete-finance-post/',
        data: {'id':id, 'csrfmiddlewaretoken':csrftoken},
        success : function(response) {
            var x="#deleteRequest"+response["id"]
            $(x).modal('hide');
            if(response["success"] === true) {
                swal("success","Finance Request Deleted Successfully","success")
                $('#finance_request_container').html(response.html);
            }
        },
        error : function() {
            alert("No Data Found");
        },
    });
}

// // Detail desciption of a post 
// function post_description(id) {
//     $.ajax({
//         type : 'POST',
//         url : '/request/finance-post-detail-page/',
//         data: {'id':id},
//         success : function(response) {
//             // var x="#deleteRequest"+response["id"]
//             // $(x).modal('toggle');
//             // $('#finance_request_container').html(response.html);
//         },
//         error : function() {
//             alert("Something went wrong")
//         }
//     });
// }