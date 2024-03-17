// Autocomplete
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('autocomplete-input');
    const resultsContainer = document.getElementById('autocomplete-results');

    const accessToken = '{{ html["finbif_access_token"] }}';

    // Todo: get from database
    const informalTaxonGroup = '{{ html["challenge"]["autocomplete"] }}';
    const endpoint = 'https://api.laji.fi/v0/autocomplete/taxon?limit=5&includePayload=true&lang=fi&informalTaxonGroup=' + informalTaxonGroup + '&excludeNameTypes=MX.hasMisspelledName,MX.hasMisappliedName&onlySpecies=true&onlyFinnish=true&access_token=' + accessToken + '&q='

    let timeoutId = null;

    input.addEventListener('input', function() {
        clearTimeout(timeoutId);

        const query = this.value.trim();
        if (!query) {
            resultsContainer.innerHTML = '';
            return; // Stop if the query is empty
        }

        timeoutId = setTimeout(() => { // Set a new timeout

            // Fetch data from API
            fetch(endpoint + encodeURIComponent(query))
                .then(response => response.json())
                .then(data => {
                    resultsContainer.innerHTML = ''; // Clear previous results

                    data.forEach(item => {
                        console.log(item); // Debugging

                        // API doesn't support excluding subspecies, variations etc, so we need to filter them out here
                        // if item.payload.taxonRankId is not MX.species, skip this item
                        if (item.payload.taxonRankId !== 'MX.species') {
                            return;
                        }

                        const div = document.createElement('div');
                        div.classList.add('autocomplete-item');
                        div.textContent = item.value + " (" + item.payload.scientificName + ")";
                        resultsContainer.appendChild(div);

                        div.addEventListener('click', function() {
                            input.value = ""; // Clear input field
                            resultsContainer.innerHTML = ''; // Clear results after selection

                            // Find the list with id="taxa"
                            const taxaList = document.getElementById('taxa');

                            // Create a new <li> element
                            const li = document.createElement('li');
                            li.innerHTML = `
                                <span class='taxon_name'>${item.value} (<em>${item.payload.scientificName}</em>)</span>
                                <input type="date" name='taxa:${item.key}' value="">
                                <a href='https://laji.fi/taxon/${item.key}' target='_blank' class='taxon_info' title='Lisätietoa: ${item.value}'>i</a>
                            `;

                            // Append the new <li> to the "taxa" list
                            taxaList.appendChild(li);
                            formIsDirty = true;

                            // Add event listeners to the newly added <li>
                            addClickListenerToLi(li);
                            addInputEventListenerToDateInput(li);
                        });
                    });
                })
                .catch(error => console.error('Error fetching data:', error));
        }, 300); // Wait before calling the API
    });
});