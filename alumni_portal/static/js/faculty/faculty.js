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
function update_form(id){
    alert(id)
$(document).on('submit','#update_request'+id,function(e) {
    e.preventDefault();
    const financial_request_form = new FormData($('update_request')[0]);
    // alert(financial_request_form)
    $.ajax({
        type : 'POST',
        url : '/request/update-finance-post/',
        data : {'form':financial_request_form,'id':id},
        processData:false,
        contentType:false,
        success : function(response){
            var x="#updateFinancialRequest"+response["id"]
            console.log(x);
            $(x).modal('hide');
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
            alert("Something went wrong")
        }
    });
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
            alert("No Data Found to delete");
        },
    });
}
//filter post
$(document).on('submit','#filter_request',function(e) {
    $('#FilterFinancialRequest').modal('hide');
    e.preventDefault();
    const financial_filter_form = new FormData($('#F')[0]);
    $.ajax({
        type : 'POST',
        url : '/request/filter-finance-post/',
        data : financial_filter_form,

        processData:false,
        contentType:false,

        success : function(response){
            $('#finance_request_container').html(response.html);
            swal({
                title: "Filter Financial",
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




// Add Chat Message to database


function addchat(id){
    // $('#addFinancialRequest').modal('hide');
    const chat = ($('#message'+id).val());
    if(chat != ""){
        console.log(id)
        console.log(chat)
        $.ajax({
            type : 'POST',
            url : '/chat/',
            data : {'chat':chat,'id':id},
            success : function(response){
                $('#messagearea').html(response.html);
            }
        }); 
    }
};

function get_form(id) {
    const csrftoken = $('[name=csrfmiddlewaretoken]').val();
    alert(id)
    $.ajax({
        type : 'POST',
        url : '/request/update-finance-post/',
        data: {'id':id,'csrftoken':csrftoken,'type':'get'},
        success : function(response) {
            console.log(response.id)
            console.log(response.html)
            $('#update_container'+response.id).html(response.html);
        },
    });
}