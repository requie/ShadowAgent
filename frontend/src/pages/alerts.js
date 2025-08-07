import { useState, useEffect } from 'react';
import axios from 'axios';

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/alerts')
      .then((res) => setAlerts(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Alerts</h1>
      <ul>
        {alerts.map((alert) => (
          <li key={alert.id} className="border-b py-2">
            <p className="font-semibold">
              {new Date(alert.timestamp).toLocaleString()}
            </p>
            <p>{alert.description}</p>
            <p>Threat ID: {alert.threat_id}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
