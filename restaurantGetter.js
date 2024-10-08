const apiKey = "AIzaSyA1sTTKpHd0qQvbSX5JMIjXSKNoaDSJnic";
const atlantaLocation = { lat: 33.7490, lng: -84.3880 }; // Latitude and Longitude for Atlanta, GA

// Function to get Atlanta restaurants using Google Places API, including pagination
function getAtlantaRestaurants(keyword = "") {
  return new Promise((resolve, reject) => {
    var atlanta = { lat: 33.7490, lng: -84.3880 };
    const request = {
      location: atlanta,
      radius: 5000,  // 5 km radius
      type: "restaurant",
      keyword: keyword // Use the keyword parameter
    };

    var service = new google.maps.places.PlacesService(document.createElement('div'));
    let allRestaurants = [];

    // Function to handle nearby search results with pagination
    const handleSearchResults = (results, status, pagination) => {
      if (status === google.maps.places.PlacesServiceStatus.OK) {
        // Add the current batch of results to the allRestaurants array
        const restaurants = results.map(place => ({
          name: place.name,
          address: place.vicinity || place.formatted_address,
          placeId: place.place_id,
          rating: place.rating,
          userRatingsTotal: place.user_ratings_total
        }));
        allRestaurants = allRestaurants.concat(restaurants);

        // If there are more results, fetch the next page after a short delay (to avoid rate limiting)
        if (pagination && pagination.hasNextPage) {
          setTimeout(() => pagination.nextPage(), 2000);
        } else {
          // No more pages, resolve the promise with all collected restaurants
          resolve(allRestaurants);
        }
      } else {
        reject(new Error(`Google Places API request failed: ${status}`));
      }
    };

    // Perform the first search request
    service.nearbySearch(request, handleSearchResults);
  });
}

// Function to test the populated restaurant array
function testRestaurantArray(restaurants) {
  if (restaurants.length === 0) {
    throw new Error("Restaurant array is empty.");
  }

  for (const restaurant of restaurants) {
    if (!restaurant.name || !restaurant.address || !restaurant.placeId) {
      throw new Error("Restaurant object missing required properties.");
    }
  }

  console.log("Restaurant array populated successfully with", restaurants.length, "restaurants:", restaurants);
}

// Main function to call and test restaurants
async function callAndTestRestaurants(keyword = "") {
  try {
    const restaurants = await getAtlantaRestaurants(keyword);
    testRestaurantArray(restaurants);
    displayRestaurants(restaurants); // Display the fetched restaurants
    return restaurants; // Return restaurants for further use if needed
  } catch (error) {
    console.error(error);
  }
}

// Function to display restaurants in the UI
function displayRestaurants(restaurants) {
  const restaurantList = document.getElementById("restaurant-list");
  restaurantList.innerHTML = ""; // Clear previous results
  restaurants.forEach(restaurant => {
    const listItem = document.createElement("li");
    listItem.textContent = `${restaurant.name} - ${restaurant.address}`;
    restaurantList.appendChild(listItem);
  });
}

// Event listener for the search button
document.addEventListener('DOMContentLoaded', () => {
  callAndTestRestaurants(); // Display all restaurants initially

  const searchButton = document.getElementById("search-button");
  searchButton.addEventListener("click", () => {
    const keyword = document.getElementById("search-input").value;
    callAndTestRestaurants(keyword); // Fetch and display filtered restaurants
  });
});