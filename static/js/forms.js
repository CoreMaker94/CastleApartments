function displayEditProfileButtonForm() {
    const form = document.getElementById("edit-profile-form");
    const profileList = document.getElementById("profile-list");
    const editProfileButton = document.getElementById("toggle-edit-profile-button");
    const isViewing = form.style.display === "none";
    form.style.display = isViewing ? "block" : "none";
    profileList.style.display = isViewing ? "none" : "block";
    editProfileButton.innerHTML = isViewing ? "Cancel Edit" : "Edit Profile";
}