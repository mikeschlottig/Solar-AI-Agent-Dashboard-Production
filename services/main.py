import uvicorn
from loguru import logger
import asyncio
from typing import Optional

# Configure logging for AI Agent Dashboard
logger.add(
    "../logs/agent_dashboard.log",
    rotation="1 day",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
)

# Configure separate log for agent activities
logger.add(
    "../logs/agent_activities.log",
    rotation="1 day",
    retention="90 days",
    level="INFO",
    filter=lambda record: "agent_activity" in record["extra"],
    format="{time:YYYY-MM-DD HH:mm:ss} | AGENT | {extra[agent_id]} | {message}"
)

class AgentDashboardServer:
    """AI Agent Dashboard Server with real-time monitoring capabilities"""
    
    def __init__(self):
        self.active_agents = {}
        self.websocket_connections = set()
        
    async def start_monitoring(self):
        """Start background monitoring tasks"""
        logger.info("Starting AI Agent Dashboard monitoring services")
        
        # Start agent health monitoring
        asyncio.create_task(self.monitor_agent_health())
        
        # Start performance metrics collection
        asyncio.create_task(self.collect_performance_metrics())
        
        # Start real-time updates
        asyncio.create_task(self.broadcast_real_time_updates())
        
    async def monitor_agent_health(self):
        """Monitor health of all registered agents"""
        while True:
            try:
                for agent_id, agent_info in self.active_agents.items():
                    # Perform health check
                    health_status = await self.check_agent_health(agent_id)
                    
                    if health_status != agent_info.get('last_health'):
                        logger.info(
                            f"Agent {agent_id} health status changed: {health_status}",
                            extra={"agent_activity": True, "agent_id": agent_id}
                        )
                        agent_info['last_health'] = health_status
                        
                await asyncio.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"Error in agent health monitoring: {e}")
                await asyncio.sleep(5)
                
    async def check_agent_health(self, agent_id: str) -> str:
        """Check health status of a specific agent"""
        # Implement actual health check logic
        # This is a placeholder implementation
        return "healthy"
        
    async def collect_performance_metrics(self):
        """Collect performance metrics for dashboard"""
        while True:
            try:
                metrics = {
                    "total_agents": len(self.active_agents),
                    "active_connections": len(self.websocket_connections),
                    "timestamp": asyncio.get_event_loop().time()
                }
                
                logger.info(f"Performance metrics collected: {metrics}")
                await asyncio.sleep(60)  # Collect every minute
            except Exception as e:
                logger.error(f"Error collecting metrics: {e}")
                await asyncio.sleep(10)
                
    async def broadcast_real_time_updates(self):
        """Broadcast real-time updates to connected WebSocket clients"""
        while True:
            try:
                if self.websocket_connections:
                    update_data = {
                        "type": "dashboard_update",
                        "agents": self.active_agents,
                        "timestamp": asyncio.get_event_loop().time()
                    }
                    
                    # Broadcast to all connected clients
                    disconnected = set()
                    for websocket in self.websocket_connections:
                        try:
                            await websocket.send_json(update_data)
                        except Exception:
                            disconnected.add(websocket)
                    
                    # Remove disconnected clients
                    self.websocket_connections -= disconnected
                    
                await asyncio.sleep(5)  # Update every 5 seconds
            except Exception as e:
                logger.error(f"Error broadcasting updates: {e}")
                await asyncio.sleep(5)

# Global dashboard server instance
dashboard_server = AgentDashboardServer()

if __name__ == "__main__":
    logger.info("Starting Solar AI Agent Dashboard backend server")
    
    # Start monitoring tasks
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(dashboard_server.start_monitoring())
    
    # Start the FastAPI server
    uvicorn.run(
        "api.bootstrap:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1,
        log_level="info",
        access_log=True,
        ws_ping_interval=20,
        ws_ping_timeout=10
    )
    
    logger.info("Solar AI Agent Dashboard server started successfully")