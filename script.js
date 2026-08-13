
const API = "http://127.0.0.1:5000";


// ================================
// LOAD DASHBOARD STATISTICS
// ================================

async function loadStats() {
    try {
        const response = await fetch(`${API}/api/stats`);
        const data = await response.json();

        document.getElementById("totalBooks").textContent =
            data.total_books;

        document.getElementById("totalCustomers").textContent =
            data.total_customers;

        document.getElementById("totalOrders").textContent =
            data.total_orders;

        document.getElementById("totalRevenue").textContent =
            "₹" + data.total_revenue.toFixed(2);

    } catch (error) {
        console.error("Error loading statistics:", error);
    }
}


// ================================
// LOAD BOOKS
// ================================

async function loadBooks() {
    try {
        const response = await fetch(`${API}/api/books`);
        const books = await response.json();

        const table = document.getElementById("booksTable");

        table.innerHTML = "";

        books.forEach(book => {

            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${book.book_id}</td>
                <td>${book.title}</td>
                <td>${book.author}</td>
                <td>${book.genre}</td>
                <td>₹${book.price}</td>
                <td>${book.stock}</td>
            `;

            table.appendChild(row);
        });

    } catch (error) {
        console.error("Error loading books:", error);
    }
}


// ================================
// LOAD CUSTOMERS
// ================================

async function loadCustomers() {
    try {
        const response = await fetch(`${API}/api/customers`);
        const customers = await response.json();

        const table = document.getElementById("customersTable");

        table.innerHTML = "";

        customers.forEach(customer => {

            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${customer.customer_id}</td>
                <td>${customer.name}</td>
                <td>${customer.email || "-"}</td>
                <td>${customer.phone || "-"}</td>
                <td>${customer.city || "-"}</td>
                <td>${customer.country || "-"}</td>
            `;

            table.appendChild(row);
        });

    } catch (error) {
        console.error("Error loading customers:", error);
    }
}


// ================================
// LOAD EVERYTHING
// ================================

loadStats();
loadBooks();
loadCustomers();

// ================================
// SALES BY GENRE CHART
// ================================

async function loadGenreChart() {
    try {
        const response = await fetch(`${API}/api/sales-by-genre`);
        const data = await response.json();

        const genres = data.map(item => item.genre);
        const sales = data.map(item => item.total_sold);

        new Chart(document.getElementById("genreChart"), {
            type: "bar",

            data: {
                labels: genres,

                datasets: [{
                    label: "Books Sold",
                    data: sales
                }]
            },

            options: {
                responsive: true,

                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });

    } catch (error) {
        console.error("Error loading genre chart:", error);
    }
}


// Load genre chart
loadGenreChart();

// ================================
// TOP 5 BOOKS CHART
// ================================

async function loadTopBooksChart() {
    try {
        const response = await fetch(`${API}/api/top-books`);
        const data = await response.json();

        const titles = data.map(item => item.title);
        const sales = data.map(item => item.total_sold);

        new Chart(document.getElementById("bookChart"), {
            type: "bar",

            data: {
                labels: titles,

                datasets: [{
                    label: "Books Sold",
                    data: sales
                }]
            },

            options: {
                indexAxis: "y",
                responsive: true,

                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });

    } catch (error) {
        console.error("Error loading top books chart:", error);
    }
}


// Load top books chart
loadTopBooksChart();
