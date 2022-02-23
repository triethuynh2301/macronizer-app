// ANCHOR - when user edit their profile and saves changes
const editProfileBtn = document.getElementById("editProfile");
let user = new User();

editProfileBtn.addEventListener("click", user.handleProfileChanges.bind(user));
