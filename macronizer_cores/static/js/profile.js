// ANCHOR - when user edit their profile and saves changes
const editProfileBtn = document.getElementById("editProfile");
let user = new User();

// editProfileBtn.addEventListener("click", function (e) {
//   e.preventDefault();

//   user.handleProfileChanges();
// });

editProfileBtn.addEventListener("click", user.handleProfileChanges.bind(user));
