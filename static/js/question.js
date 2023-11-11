const q_comment_edit_icon = document.getElementById("qc-edit");
    q_comment_edit_icon.addEventListener("click", function() {
        q_comment_edit();
    });

function q_comment_edit() {
    let text = event.target.getAttribute('name');        
    document.getElementById("q-comment").value = document.getElementById(text).textContent;
    document.getElementById("q-comment-id").value = text.slice(1);
    document.getElementById("q-comment-button").value = "Edit Comment"

}
