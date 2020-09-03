import { usePlugin } from '@nomiclabs/buidler/config';

module.exports = {
  paths: {
    artifacts: './build',
  },

  solc: {
    version: '0.6.10',
    optimizer: {
      enabled: true,
      runs: 999999,
    },
    evmVersion: 'istanbul',
  },
};
