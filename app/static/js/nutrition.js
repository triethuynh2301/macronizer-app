let foodItemList = [];

// SECTION datetime picker component
const dateTimePickerInput = document.querySelector(".datepicker_input");
const datepicker = new Datepicker(dateTimePickerInput, {
  format: "mm/dd/yyyy",
  todayHighlight: true,
  calendarWeeks: true,
});

// ANCHOR - When nutrition page loads -> load meals logged for today
window.addEventListener("load", handleLoadLog);

// ANCHOR - When user picks a date to view food log -> load meals for date picked
dateTimePickerInput.addEventListener("changeDate", handleLoadLog);

/*************************************************
 * - Clear current log                           *
 * - Make API call to fetch log for date picked  *
 * - Make UI components for meal and add to page *
 * - Display picked date on search food modal    *
 *************************************************/
async function handleLoadLog() {
  clearMealList();

  // format chosen date on datetimepicker to yy/mm/dd
  const dateString = formatDate();

  // API call
  const meals = await Log.searchLogByDate(dateString);

  // add meal component to UI
  addMealsToPage(meals);

  // display picked date for food search moodal
  const searchFoodLabel = document.getElementById("searchFoodLabel");
  searchFoodLabel.textContent = datepicker
    .getDate()
    .toLocaleDateString("en-US", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "2-digit",
    });
}

// ANCHOR - When user click on search food icon -> search for food from API
const searchFoodBtn = document.getElementById("searchFoodBtn");
searchFoodBtn.addEventListener("click", handleSearchFood);

/***********************************************************************
 *  * - Clear current food search results                              *
 *  * - Make API call to CaloriesNinja for food info with query string *
 *  * - Make UI component for food item and add to page                *
 * @param {Event} - event                                              *
 ***********************************************************************/
async function handleSearchFood(e) {
  // prevent page reloading
  e.preventDefault();

  // remove previous search contents
  clearFoodSearchTable();

  // enable loading spinner
  const loadingSpinner = document.querySelector("#loading-icon");
  loadingSpinner.classList.toggle("d-none");

  // API call
  const queryString = document.querySelector(
    ".nutrition .search-form input"
  ).value
  const foodItems = await FoodItem.searchFoodItem(queryString);
  // if (foodItems.length === 0) {
  //   // TODO - add message to let user know nothing matches search 
  //   return;
  // }
  foodItemList = foodItems;

  // disable loading spinner and add food item component to UI
  loadingSpinner.classList.toggle("d-none");
  addFoodItemToPage(foodItems);
}

// ANCHOR - When user clicks on log food btn to log their meals
const logFoodBtn = document.getElementById("logFoodBtn");
logFoodBtn.addEventListener("click", handleLogFood);

/*********************************************
 * - Get meal no and date to log from UI     *
 * - Make API post request with json payload *
 * - Fetch new log to reflect changes        *
 *********************************************/
async function handleLogFood() {
  // no food to log -> do nothing
  if (foodItemList.length === 0) {
    return;
  }

  // get date and meal no from UI
  const dateString = formatDate();
  const select = document.querySelector(".form-select");
  const mealNo = select.options[select.selectedIndex].value;

  // API call
  res = await Log.logMeal(mealNo, dateString, foodItemList);
  // clear the search result array after logging food
  foodItemList = [];

  // fetch new log to reflect changes
  handleLoadLog();
}

// ANCHOR - When user starts dragging food items from one meal to another
const foodList = document.querySelectorAll(".food-list");
foodList.forEach((item) => {
  item.addEventListener("dragstart", handleDragStart);
});

// ANCHOR - When user drags over/drops food items
const meals = document.querySelectorAll(".meal");
meals.forEach((item) => {
  item.addEventListener("dragover", handleDragOverEmptyMeal);
  item.addEventListener("drop", handleDropOnEmptyMeal);
});

/**************************************************************************
 * * - Store the drag's data into dataTransfer object for later retrieval *
 * * @param {Event} - event*                                             *
 **************************************************************************/
function handleDragStart(e) {
  // initiate event only if selected target is a food item
  if (e.target.tagName !== "LI") {
    return;
  }

  // store the id of the item
  e.dataTransfer.setData("text/plain", e.target.id);
}

/*******************************************************
 * - Disable default behavior to enale dragging action *
 * @param {Event} - e                                 *
 *******************************************************/
function handleDragOverEmptyMeal(e) {
  e.preventDefault();
}

/************************************************************
 * - Drop the item to correct drop zone                     *
 * - Make API call to update food item to according meal no *
 * @param {Event} - e                                      *
 ************************************************************/
async function handleDropOnEmptyMeal(e) {
  if (e.target.tagName !== "H3") {
    return;
  }

  // get date from UI
  const dateString = formatDate();

  // get the draggable element
  const id = e.dataTransfer.getData("text/plain");
  const draggable = document.getElementById(id);
  const foodItemId = draggable.id;

  // add it to the dragged target
  e.target.nextElementSibling.append(draggable);
  const mealNo = e.target.nextElementSibling.dataset.mealNo;

  // make API call
  await Log.updateLoggedMeal(mealNo, dateString, foodItemId);

  // display the draggable element
  draggable.classList.remove("hide");
}
