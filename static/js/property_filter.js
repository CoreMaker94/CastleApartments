document.addEventListener("DOMContentLoaded", function () {
  function registerSearchButtonhandler() {
    const searchButton = document.getElementById("search-icon");

    searchButton.addEventListener("click", async function () {
      const search = document.getElementById("search-value").value.trim();
      const zipcode = document.getElementById("zipcode-filter")?.value || "";
      const propertyType = document.getElementById("type-filter")?.value || "";
      const priceOrder = document.getElementById("price-filter")?.value || "";
      const propertiesPlaceholder = document.getElementById("property-grid");

      const query = new URLSearchParams({
        search_filter: search,
        zipcode: zipcode,
        property_type: propertyType,
        price_order: priceOrder,
      });

      try {
        const response = await fetch(`?${query.toString()}`);

        if (response.ok) {
          const json = await response.json();
          const properties = json.data;

          let html = "";

          if (properties.length > 0) {
            html = properties.map((property) => `
              <div class="col-md-4 mb-4">
                <div class="card h-100 shadow-sm">
                  <img src="${property.image}" class="card-img-top" alt="Property Image">
                  <div class="card-body">
                    <h5 class="card-title">${property.address}</h5>
                    <p class="card-text">${property.beds} 🛏️ • ${property.bath} 🛁 • ${property.size} 📐</p>
                    <p class="card-text"><strong>$${property.price}</strong></p>
                    <a href="/property/${property.id}" class="btn btn-primary btn-sm">View Details</a>
                  </div>
                </div>
              </div>
            `).join("");
          } else {
            html = `
              <div class="col-12 text-center mt-4">
                <div class="alert alert-warning" role="alert">
                  No properties found matching your criteria.
                </div>
              </div>
            `;
          }

          propertiesPlaceholder.innerHTML = html;
        } else {
          propertiesPlaceholder.innerHTML = "<p class='text-danger'>Failed to load properties.</p>";
        }
      } catch (error) {
        console.error("Error fetching properties:", error);
      }
    });
  }

  registerSearchButtonhandler();
});
