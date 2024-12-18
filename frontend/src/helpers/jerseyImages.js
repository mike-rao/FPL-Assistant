const requireContext = require.context('../images/jerseys', false, /\.(png|jpe?g|svg)$/);

const jerseyImages = {};

requireContext.keys().forEach((fileName) => {
  const teamName = fileName
    .replace('./', '')
    .replace(/\.(png|jpe?g|svg)$/, '');

  jerseyImages[teamName] = requireContext(fileName);
});

export default jerseyImages;