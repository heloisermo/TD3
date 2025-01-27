const express = require('express');
const app = express();

app.get('/getServer', (req, res) => {
    res.json({ code: 200, server: "localhost:3001" });
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`DNS server running on http://localhost:${PORT}`);
});
