S3-->lambda-->bedrock-->openai-->response-->lambda-->doc-store to S3
version: '3.8'

services:
  cortex:
    image: thehiveproject/cortex:latest
    container_name: cortex
    ports:
      - "8088:8088"
    volumes:
      - C:/cortex-setup/cortex/config:/cortex/config
    environment:
      - CORTEX_CONFIG_FILE=/cortex/config/config.yaml
    networks:
      - cortex-network

networks:
  cortex-network:
    driver: bridge
