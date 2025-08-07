import { useEffect, useState } from 'react';
import axios from 'axios';
import { Bar, Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip, Legend, ArcElement } from 'chart.js';

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend, ArcElement);

export default function Home() {
  const [threats, setThreats] = useState([]);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    // Fetch threats
    axios.get('http://localhost:8000/threats')
      .then((res) => {
        setThreats(res.data);
      })
      .catch((err) => console.error(err));

    // Fetch alerts
    axios.get('http://localhost:8000/alerts')
      .then((res) => {
        setAlerts(res.data);
      })
      .catch((err) => console.error(err));
  }, []);

  // Prepare chart data
  const threatTypeCounts = threats.reduce((acc, threat) => {
    const t = threat.threat_type;
    acc[t] = (acc[t] || 0) + 1;
    return acc;
  }, {});

  const barData = {
    labels: Object.keys(threatTypeCounts),
    datasets: [
      {
        label: 'Threat Count',
        data: Object.values(threatTypeCounts),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
      }
    ]
  };

  const doughnutData = {
    labels: Object.keys(threatTypeCounts),
    datasets: [
      {
        data: Object.values(threatTypeCounts),
        backgroundColor: ['#e74c3c', '#f1c40f', '#3498db'],
      }
    ]
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>ShadowAgent Dashboard</h1>
      <section>
        <h2>Active Threats</h2>
        <ul>
          {threats.map((threat) => (
            <li key={threat.id}>
              <strong>{threat.title}</strong> – {threat.description} ({threat.threat_type})
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Alerts</h2>
        <ul>
          {alerts.map((alert) => (
            <li key={alert.id}>
              {alert.description} – threat #{alert.threat_id}
            </li>
          ))}
        </ul>
      </section>

      <section style={{ maxWidth: '600px' }}>
        <h2>Threat Types Distribution</h2>
        <Bar data={barData} />
        <Doughnut data={doughnutData} />
      </section>
    </div>
  );
}
