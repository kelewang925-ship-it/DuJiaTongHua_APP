const API_MODE = 'mock';

export function getApiMode() {
  return API_MODE;
}

export async function delay(ms = 300) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function requestMock(data, ms = 300) {
  await delay(ms);
  return {
    success: true,
    data,
  };
}
