// SECTION meals logged component (for nutrition page)
function createMealComponent(foodItem) {
  const liEl = document.createElement("li");
  liEl.addEventListener("mouseenter", handleMouseEnter);
  liEl.addEventListener("mouseleave", handleMouseLeave);
  liEl.className = "ps-3 m-0 w-50";
  liEl.setAttribute("draggable", true);
  liEl.id = foodItem.id;

  const foodNameEl = document.createElement("small");
  foodNameEl.className = "fw-bolder p-0 m-0 text-capitalize";
  foodNameEl.textContent = foodItem.name;
  liEl.appendChild(foodNameEl);

  const divEl = document.createElement("div");
  divEl.className = "d-flex gap-3";
  liEl.appendChild(divEl);

  const amountEl = document.createElement("small");
  amountEl.textContent = `${foodItem.serving_size_gram} g`;
  divEl.appendChild(amountEl);

  const caloriesEl = document.createElement("small");
  caloriesEl.textContent = `${foodItem.calories} cals`;
  divEl.appendChild(caloriesEl);

  const deleteIcon = document.createElement("i");
  deleteIcon.className =
    "fa-regular fa-trash-can ms-auto text-secondary visually-hidden";
  deleteIcon.addEventListener("click", handleDeleteFoodItem);
  divEl.appendChild(deleteIcon);

  return liEl;
}

async function handleDeleteFoodItem(e) {
  if (e.target.tagName !== "I") return;

  // get food id
  const foodId = e.target.parentNode.parentNode.id;

  // make API call to DELETE food item
  await FoodItem.deleteFoodItem(foodId);

  // reload page to reflect changes
  // TODO - refactor to make individual changes
  handleLoadLog();
}

// Show the delete icon on hover
function handleMouseEnter(e) {
  if (e.target.tagName !== "LI") {
    return;
  }

  // get food item id
  const foodId = e.target.id;

  // show the delete icon and allow users to delete food item on click
  e.target.children[1].children[2].classList.toggle("visually-hidden");
}

// Hide the delete icon after hovering
function handleMouseLeave(e) {
  if (e.target.tagName !== "LI") {
    return;
  }

  e.target.children[1].children[2].classList.toggle("visually-hidden");
}

// SECTION food item table component (nutrition page)

/***********************************************
 * - Create food item table component          *
 * @param {FoodItem} - FoodItem object         *
 * @return {HTMLElement} - table row component *
 ***********************************************/
function createFoodItemsTableComponent(foodItem) {
  const row = document.createElement("tr");

  const nameColumn = document.createElement("td");
  nameColumn.className = "text-capitalize";
  nameColumn.textContent = foodItem.name;
  row.appendChild(nameColumn);

  const servingColumn = document.createElement("td");
  servingColumn.textContent = `${foodItem.servingSize}g`;
  row.appendChild(servingColumn);

  const proteinColumn = document.createElement("td");
  proteinColumn.textContent = `${foodItem.protein}g`;
  row.appendChild(proteinColumn);

  const fatColumn = document.createElement("td");
  fatColumn.textContent = `${foodItem.totalFat}g`;
  row.appendChild(fatColumn);

  const carbColumn = document.createElement("td");
  carbColumn.textContent = `${foodItem.carbohydrate}g`;
  row.appendChild(carbColumn);

  const calsColumn = document.createElement("td");
  calsColumn.textContent = `${foodItem.calories} cals`;
  row.appendChild(calsColumn);

  return row;
}
