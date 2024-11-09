<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trading Platform</title>
</head>
<body>
    <h1>Trading Platform</h1>
    <div>
        <h2>Login</h2>
        <input type="text" id="username" placeholder="Username">
        <button onclick="login()">Login</button>
    </div>
    <div>
        <h2>Balance</h2>
        <button onclick="getBalance()">Get Balance</button>
        <p id="balance"></p>
    </div>
    <div>
        <h2>Buy Stock</h2>
        <input type="text" id="stock" placeholder="Stock Symbol">
        <input type="number" id="amount" placeholder="Amount">
        <button onclick="buyStock()">Buy</button>
    </div>

    <script>
        function login() {
            const username = document.getElementById('username').value;
            fetch('/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username})
            }).then(response => response.json())
              .then(data => alert(data.message));
        }

        function getBalance() {
            const username = document.getElementById('username').value;
            fetch(`/balance?username=${username}`)
                .then(response => response.json())
                .then(data => document.getElementById('balance').innerText = `Balance: $${data.balance}`);
        }

        function buyStock() {
            const username = document.getElementById('username').value;
            const stock = document.getElementById('stock').value;
            const amount = parseInt(document.getElementById('amount').value);
            fetch('/buy', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, stock, amount})
            }).then(response => response.json())
              .then(data => alert(data.message));
        }
    </script>
</body>
</html>
