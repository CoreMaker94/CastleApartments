document.addEventListener('DOMContentLoaded', function () {
  function registerSearchButtonHandler() {
    const searchButton = document.getElementById("search-icon");

    searchButton.addEventListener("click", async function () {
      const formatter = new Intl.NumberFormat('de-DE');
      const form = document.getElementById("filter-form");
      const propertiesPlaceholder = document.getElementById("property-grid");

      const checkedZips = form.querySelectorAll('input[type="checkbox"][name="zipcodes"]:checked');
      const checkedTypes = form.querySelectorAll('input[type="checkbox"][name="property_types"]:checked');

      const selectedZipcodes = Array.from(checkedZips).map(cb => cb.value);
      const selectedTypes = Array.from(checkedTypes).map(cb => cb.value);

      const search = document.getElementById("search-value").value.trim();
      const order_by = document.getElementById("order_by").value;
      const min_price = document.getElementById("min-price")?.value;
      const max_price = document.getElementById("max-price")?.value;

      // ✅ Validate price range before fetching
      if (min_price && max_price && parseInt(min_price) > parseInt(max_price)) {
        propertiesPlaceholder.innerHTML = `
          <div class="col-12 text-center mt-4">
            <div class="alert alert-danger" role="alert">
              Minimum price cannot be greater than maximum price.
            </div>
          </div>
        `;
        return; // ⛔ Stop fetch if validation fails
      }

      const zipParam = encodeURIComponent(selectedZipcodes.join(","));
      const typeParam = encodeURIComponent(selectedTypes.join(","));
      const searchParam = encodeURIComponent(search);
      const orderParam = encodeURIComponent(order_by);
      const minPriceParam = encodeURIComponent(min_price);
      const maxPriceParam = encodeURIComponent(max_price);

      const query = `?zip_filter=${zipParam}&type_filter=${typeParam}&address_name=${searchParam}&order_by=${orderParam}&min_price=${minPriceParam}&max_price=${maxPriceParam}`;

      try {
        const response = await fetch(`${query}`);
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
                    <p class="card-text"><strong>${formatter.format(property.price)}<strong/></p>
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
          const errorData = await response.json();
          propertiesPlaceholder.innerHTML = `
            <div class="col-12 text-center mt-4">
              <div class="alert alert-danger" role="alert">
                ${errorData.error || "Failed to load properties."}
              </div>
            </div>
          `;
        }
      } catch (error) {
        console.error("Error fetching properties:", error);
      }
    });
  }

  registerSearchButtonHandler();
});

function toggleDropdown1() {
  document.getElementById('ZipcodeDropdown').classList.toggle("show");
}

function toggleDropdown2() {
  document.getElementById('TypeDropdown').classList.toggle("show");
}

document.addEventListener('click', (e) => {
  const zipbutton = document.getElementById('ZipcodeDropdown');
  const typebutton = document.getElementById('TypeDropdown');
  if (!zipbutton.contains(e.target)) zipbutton.classList.remove("show");
  if (!typebutton.contains(e.target)) typebutton.classList.remove("show");
});
