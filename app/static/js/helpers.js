/*************************************************************************
 * - Format chosen date from datepicker componenet to YYYY-MM-DD         *
 * @return {String} - string representation of date in format YYYY-MM-DD *
 *************************************************************************/
function formatDate() {
  let date = new Date(datepicker.getDate());
  let year = new Intl.DateTimeFormat("en", { year: "numeric" }).format(date);
  let month = new Intl.DateTimeFormat("en", { month: "numeric" }).format(date);
  let da = new Intl.DateTimeFormat("en", { day: "2-digit" }).format(date);
  return `${year}-${month}-${da}`;
}

// SECTION helper methods for displaying meals logged data

/***************************************
 * - Make UI component for meal        *
 * - Add to page according to meal no  *
 * @param {meals} - List of Log object *
 ***************************************/
function addMealsToPage(meals) {
  meals.forEach((meal) => {
    meal.foodItems.forEach((item) => {
      const mealComponent = createMealComponent(item);
      addMealComponentToPage(meal.mealNo, mealComponent);
    });
  });
}

/*****************************************
 * - Add meal to UI according to meal no *
 *****************************************/
function addMealComponentToPage(mealNo, mealComponent) {
  if (mealNo === 1) {
    const mealOne = document.querySelector('[data-meal-no="1"]');
    mealOne.appendChild(mealComponent);
  } else if (mealNo === 2) {
    const mealTwo = document.querySelector('[data-meal-no="2"]');
    mealTwo.appendChild(mealComponent);
  } else if (mealNo === 3) {
    const mealTwo = document.querySelector('[data-meal-no="3"]');
    mealTwo.appendChild(mealComponent);
  } else if (mealNo === 4) {
    const mealTwo = document.querySelector('[data-meal-no="4"]');
    mealTwo.appendChild(mealComponent);
  } else if (mealNo === 5) {
    const mealTwo = document.querySelector('[data-meal-no="5"]');
    mealTwo.appendChild(mealComponent);
  }
}

/*********************************
 * - Clear the log for all meals *
 *********************************/
function clearMealList() {
  const mealList = document.getElementsByClassName("food-list");
  for (let meal of mealList) {
    while (meal.firstChild) {
      meal.firstChild.remove();
    }
  }
}

// SECTION helper methods for displaying food search results from API

/********************************************************
 * - Clear previous search results from food item table *
 ********************************************************/
function clearFoodSearchTable() {
  const tableBody = document.querySelector(".food-item-table");
  while (tableBody.firstChild) {
    tableBody.firstChild.remove();
  }
}

/*********************************************************
 * - Make UI table components for food item              *
 * - Add component to page                               *
 * - Adjust nutrition report according to search results *
 * @param {FoodItem[]} items - list of FoodItem objects  *
 *********************************************************/
function addFoodItemToPage(items) {
  let totalCals = 0;
  let totalPro = 0;
  let totalFatReport = 0;
  let totalCarb = 0;

  items.forEach((item) => {
    const { calories, protein, totalFat, carbohydrate } = item;
    totalCals += calories;
    totalPro += protein;
    totalFatReport += totalFat;
    totalCarb += carbohydrate;

    const foodItemComponent = createFoodItemsTableComponent(item);
    addFoodItemComponentToPage(foodItemComponent);
  });

  adjustFoodReport(totalCals, totalPro, totalFatReport, totalCarb);
}

/******************************************************
 * * - Add food item HTML to page                     *
 * * @param {HTMLElement} - food item HTML component* *
 ******************************************************/
function addFoodItemComponentToPage(foodItemComponent) {
  const tableBody = document.querySelector(".food-item-table");
  tableBody.append(foodItemComponent);
}

/********************************************************
 * - Display total nutrition for current search results *
 * @param {Number} cals - total amount of calories      *
 * @param {Number} protein - total amount of protein    *
 * @param {Number} fat - total amount of fat            *
 * @param {carb} carb - total amount of carb            *
 ********************************************************/
function adjustFoodReport(cals, protein, fat, carb) {
  const calsReport = document.querySelector(".total-calories");
  const proteinReport = document.querySelector(".total-protein");
  const fatReport = document.querySelector(".total-fat");
  const carbReport = document.querySelector(".total-carb");

  calsReport.textContent = cals;
  proteinReport.textContent = protein;
  fatReport.textContent = fat;
  carbReport.textContent = carb;
}
