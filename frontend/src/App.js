import './App.css';
import { DataProvider } from './context/DataContext';
import ControlsView from './components/views/ControlsView';
import KeyDisplayView from './components/views/KeyDisplayView';
import AddressDisplayView from './components/views/AddressDisplayView';
import StepsTableView from './components/views/StepsTableView';
import VisualizationView from './components/views/VisualizationView'; // Import VisualizationView

function App() {
  return (
    <DataProvider>
      <div className="App">
        <header className="App-header">
          <h1>Base40 Symbolic-Angular Crypto Suite</h1>
        </header>

        <div className="content-wrapper">
          <ControlsView />
          <KeyDisplayView />
          <AddressDisplayView />
          <VisualizationView /> {/* Use VisualizationView */}
          <StepsTableView />
        </div>

        <footer style={{ marginTop: '30px', paddingTop: '20px', borderTop: '1px dashed #008000' }}>
          <p>© 2023 Base40 Project - Matrix Themed Frontend</p>
        </footer>
      </div>
    </DataProvider>
  );
}

export default App;
