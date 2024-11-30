const requireContext = require.context('../images/jerseys', false, /\.(png|jpe?g|svg)$/);

const jerseyImages = {};

// Dynamically build the `jerseyImages` object
requireContext.keys().forEach((fileName) => {
  // Extract the team name without './' and file extension
  const teamName = fileName
    .replace('./', '') // Remove './' from the file name
    .replace(/\.(png|jpe?g|svg)$/, ''); // Remove the file extension

  // Use `requireContext` to resolve the path
  jerseyImages[teamName] = requireContext(fileName);
});

export default jerseyImages;