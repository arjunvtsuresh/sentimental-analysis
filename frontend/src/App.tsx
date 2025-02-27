import SentimentForm from "./components/SentimentForm";
import { Container, Typography , CssBaseline , Box , Paper , createTheme} from "@mui/material";


function App() {
  return (
      <Container maxWidth="sm">
          <Paper elevation={1} sx={{ p: 4, textAlign: "center" , backgroundColor:'whitesmoke'}}>
            <Typography variant="h5" gutterBottom>
              Sentiment Analysis
            </Typography>
            <SentimentForm />
          </Paper>
      </Container>
  );
}

export default App;