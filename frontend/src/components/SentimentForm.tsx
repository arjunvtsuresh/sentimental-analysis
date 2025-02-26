import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import { gql, useLazyQuery } from "@apollo/client";
import { TextField, Button, Typography, Box } from "@mui/material";

// GraphQL Query
const GET_SENTIMENT = gql`
  query GetSentiment($text: String!, $apiKey: String!) {
    sentiment(text: $text, apiKey: $apiKey)
  }
`;

// Validation Schema
const schema = yup.object({
  text: yup
    .string()
    .trim()
    .min(3, "Text must be at least 3 characters")
    .max(10000, "Text must be less than 200 characters")
    .required("Text is required"),
});

export default function SentimentForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(schema),
  });

  const [getSentiment, { loading, data, error }] = useLazyQuery(GET_SENTIMENT);

  const onSubmit = (formData: { text: string }) => {
    getSentiment({ variables: { text: formData.text, apiKey: "mysecretkey" } });
  };

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmit)} textAlign="center">
      
      
      <TextField
        label="Enter text"
        variant="outlined"
        fullWidth
        margin="normal"
        {...register("text")}
        error={!!errors.text}
        helperText={errors.text?.message}
      />
      
      <Button type="submit" variant="contained" color="primary" disabled={loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </Button>

      {error && <Typography color="error">Error: {error.message}</Typography>}
      {data && <Typography>Sentiment: {data.sentiment}</Typography>}
    </Box>
  );
}
