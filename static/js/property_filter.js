document.addEventListener("DOMContentLoaded", function () {
  function registerSearchButtonhandler() {
    const searchButton = document.getElementById("search-icon");

    searchButton.addEventListener("click", async function () {
      const searchValueElement = document.getElementById("search-value");
      const propertiesPlaceholder = document.getElementById("property-grid");
      const value = searchValueElement.value.trim();

      try {
        const response = await fetch(`?search_filter=${encodeURIComponent(value)}`);
        if (response.ok) {
          const json = await response.json();
          const properties = json.data;

          const html = properties
            .map(
              (property) => `
                <div class="property-card">
                  <h3>${property.address}</h3>
                  <p>Zip Code: ${property.zipcode.code || property.zipcode}</p>
                  <p>Type: ${property.type.name || property.type}</p>
                  <p>Price: $${property.price}</p>
                  <img src="${property.image}" alt="Property Image" style="max-width: 100%; height: auto;" />
                  <a href="/property/${property.id}" class="btn btn-primary btn-sm">View Details</a>
                </div>
              `
            )
            .join("");

          propertiesPlaceholder.innerHTML = html;
        } else {
          propertiesPlaceholder.innerHTML = "<p>Failed to load properties.</p>";
        }
      } catch (error) {
        console.error("Error fetching properties:", error);
      }
    });
  }

  registerSearchButtonhandler();
});
