
function formSubmit(onclick, form_id, location, display, modal_type) {

    $('.' + onclick).click(function() {
    var form = document.querySelector("#" + form_id);

    if (!form.checkValidity()) {
        var tmpSubmit = document.createElement('button');
        form.appendChild(tmpSubmit);
        tmpSubmit.click();
        form.removeChild(tmpSubmit);
    } else {
        $.ajax({
            url: "/" + location,
            type: "POST",
            data: $("#" + form_id).serialize(),
            success: function(response) {
                    $('#' + display).html(response);
            }
        });

        if(modal_type == "off") {
        var modal = document.getElementById("myModal");
            modal.style.display = "none";
        } else if (modal_type == "on") {
            var modal = document.getElementById("myModal");
            modal.style.display = "block";
        }

    }
    });
};


function table_toggle (onclick, table_id, table_alter) {
    $('.' + onclick).click(function() {

    if($("#" + table_id).css('display') == 'none')
    {
        $("#" + table_id).show();
        $("#" + table_alter).hide();
    } else {
        $("#" + table_id).hide();
        $("#" + table_alter).show();
    }

    });
};


function acct_toggle(onclick, show_id, hide_id) {
    $('.' + onclick).click(function() {
        $("#" + show_id).toggle();
        $("#" + hide_id).toggle();
    });
}



function modalLoad() {

    // Get the modal
    var modal = document.getElementById("myModal");

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
}


function modal_navigate() {
    var modal = document.getElementById("myModal");

        // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }

    $('.modal_navigate').click(function() {
        var type = this.value;

        $.ajax({
        url: "/" + type,
        type: "GET",
        success: function(response) {
            $("#modal_display").html(response);
            modal.style.display = "block";
          }
        });
    });
};


function modal_param() {

    var form_modal = document.getElementById("myModal");

        // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == form_modal) {
        form_modal.style.display = "none";
      }
    }

    $('.form_navigate').click(function() {

        var type = this.value;
        var key = this.name;

        $.ajax({
        url: "/" + type + "?key=" + key,
        type: "GET",
        success: function(response) {
            $("#modal_display").html(response);
            form_modal.style.display = "block";
          }
        });
    });


};


function follow_view() {

    var form_modal = document.getElementById("myModal");

        // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == form_modal) {
        form_modal.style.display = "none";
      }
    }

    $("#table_id").on("click", '.follow_view', (function() {

        var key = this.value;

        $.ajax({
        url: "/view_followup" + "?key=" + key,
        type: "GET",
        success: function(response) {
            $("#modal_display").html(response);
            form_modal.style.display = "block";
          }
        });
    }));
};

function update_acct_detail() {

    $('.acct_detail').click(function() {
    var acct_id = this.name;
        $.ajax({
            url: "/update_acct_detail?acct_id=" + acct_id,
            type: "POST",
            data: $("#acct_detail").serialize(),
            success: function(response) {
                    alert(response)
            }
        });
    });
};