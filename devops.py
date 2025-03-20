import typer
import subprocess

app = typer.Typer()

@app.command()
def svc_port_forward(
    namespace: str = typer.Option(..., help="Namespace to deploy to"), 
    service: str = typer.Option(..., help="Service name"),
    port_mappings: str = typer.Option(..., help="Port mappings in the form 'host_port:target_port,host_port:target_port'")
):
    # Split the port mappings into a list of 'host_port:target_port' strings
    port_list = port_mappings.split(',')

    # Build the kubectl port-forward command
    port_forward_command = ["kubectl", "port-forward", f"svc/{service}", "--namespace", namespace]

    # Add each port mapping to the command
    for port_mapping in port_list:
        # Ensure the port mapping is in the correct format 'host_port:target_port'
        try:
            host_port, target_port = port_mapping.split(':')
            port_forward_command.append(f"{host_port}:{target_port}")
        except ValueError:
            typer.echo(f"Invalid port mapping format: {port_mapping}. It should be 'host_port:target_port'")
            return

    # Print out the command for confirmation
    typer.echo(f"Running command: {' '.join(port_forward_command)}")

    try:
        # Run the kubectl port-forward command
        subprocess.run(port_forward_command, check=True)
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error occurred while port-forwarding: {e}")
    except FileNotFoundError:
        typer.echo("kubectl is not installed or not found in the system path.")
    except Exception as e:
        typer.echo(f"Unexpected error: {e}")
        
@app.command()
def set(
    namespace: str = typer.Option(..., help="Namespace to set in the kubeconfig"),
    context: str = typer.Option(None, help="Kubeconfig context to set (optional)"),
):
    if context:
        # Construct the kubectl command to set the context and namespace
        set_context_namespace_command = [
            "kubectl", "config", "set-context", context, "--namespace", namespace
        ]
        typer.echo(f"Setting context '{context}' and namespace '{namespace}'")
    else:
        # Construct the kubectl command to set only the namespace for the current context
        set_context_namespace_command = [
            "kubectl", "config", "set-context", "--current", "--namespace", namespace
        ]
        typer.echo(f"Setting namespace '{namespace}' for the current context")

    try:
        # Run the kubectl command to set the context and namespace
        subprocess.run(set_context_namespace_command, check=True)
        typer.echo(f"Successfully set context and namespace.")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error occurred while setting the context and namespace: {e}")
    except FileNotFoundError:
        typer.echo("kubectl is not installed or not found in the system path.")
    except Exception as e:
        typer.echo(f"Unexpected error: {e}")
    
#Check cluster info
def cluster_info():
    try:
        # Run the command to get current context and cluster info
        result = subprocess.run(["kubectl", "config", "current-context"], capture_output=True, text=True, check=True)
        typer.echo(f"Current context: {result.stdout.strip()}")
        result = subprocess.run(["kubectl", "cluster-info"], capture_output=True, text=True, check=True)
        typer.echo(f"Cluster info: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error occurred while fetching cluster info: {e}")
    except FileNotFoundError:
        typer.echo("kubectl is not installed or not found in the system path.")

#Get All Pods in a Namespace with Filtering
@app.command()
def list_pods(namespace: str, label: str = None, status: str = None):
    command = ["kubectl", "get", "pods", "--namespace", namespace]
    if label:
        command.append(f"--selector={label}")
    if status:
        command.append(f"--field-selector=status.phase={status}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error fetching pods: {e}")

# Port Forward to a Pod (Directly)
@app.command()
def port_forward_pod(namespace: str, pod_name: str, host_port: int, container_port: int):
    port_forward_command = [
        "kubectl", "port-forward", f"pod/{pod_name}", f"{host_port}:{container_port}", "--namespace", namespace
    ]
    try:
        subprocess.run(port_forward_command, check=True)
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error occurred while port-forwarding to pod: {e}")
        
# Scaling Deployments
@app.command()
def scale_deployment(namespace: str, deployment_name: str, replicas: int):
    scale_command = [
        "kubectl", "scale", "deployment", deployment_name, f"--replicas={replicas}", "--namespace", namespace
    ]
    try:
        subprocess.run(scale_command, check=True)
        typer.echo(f"Successfully scaled {deployment_name} to {replicas} replicas.")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error scaling deployment: {e}")

@app.command()
def view_logs(namespace: str, pod_name: str, container: str = None, tail: int = 100):
    command = ["kubectl", "logs", pod_name, "--namespace", namespace, f"--tail={tail}"]
    if container:
        command.append(f"--container={container}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error viewing logs: {e}")


@app.command()
def delete_resource(namespace: str, resource_type: str, resource_name: str):
    delete_command = ["kubectl", "delete", resource_type, resource_name, "--namespace", namespace]
    try:
        subprocess.run(delete_command, check=True)
        typer.echo(f"Successfully deleted {resource_type} {resource_name}.")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error deleting resource: {e}")
        
@app.command()  
def get_resource_usage(namespace: str):
    command = ["kubectl", "top", "pod", "--namespace", namespace]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error fetching resource usage: {e}")

@app.command()
def create_namespace(namespace: str):
    create_command = ["kubectl", "create", "namespace", namespace]
    try:
        subprocess.run(create_command, check=True)
        typer.echo(f"Namespace {namespace} created successfully.")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error creating namespace: {e}")

#Exec into a Pod (Interactive Shell)       
@app.command()
def exec_pod(namespace: str = typer.Option(..., help="Namespace to set in the kubeconfig"), pod_name: str = typer.Option(..., help="Pod name to exec into"), container: str = None , command: str = typer.Option(..., help="Command to use for exec example: /bin/bash")):
    exec_command = ["kubectl", "exec", "-it", pod_name, "--namespace", namespace, "--", command]
    if container:
        exec_command.append(f"--container={container}")
    try:
        subprocess.run(exec_command, check=True)
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error execing into pod: {e}")


@app.command()
def get(
    cluster_info: bool = typer.Option(False, help="Get cluster info"),
    pods: bool = typer.Option(False, help="List pods"),
    namespace: str = typer.Option(None, help="Specify a namespace for pods"),
):
    if cluster_info:
        try:
            # Get the current context
            context_result = subprocess.run(
                ["kubectl", "config", "current-context"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            typer.echo(f"Current context: {context_result.stdout.strip()}")

            # Get cluster info
            cluster_result = subprocess.run(
                ["kubectl", "cluster-info"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            typer.echo(f"Cluster info:\n{cluster_result.stdout.strip()}")

        except subprocess.CalledProcessError as e:
            typer.echo(f"Error occurred while fetching cluster info: {e}")
        except FileNotFoundError:
            typer.echo("kubectl is not installed or not found in the system path.")

    if pods:
        try:
            # Build the command to get pods
            command = ["kubectl", "get", "pods"]
            if namespace:  # If a namespace is specified, add it to the command
                command.extend(["--namespace", namespace])

            pods_result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            typer.echo(f"Pods {'in namespace ' + namespace if namespace else 'across all namespaces'}:\n{pods_result.stdout.strip()}")

        except subprocess.CalledProcessError as e:
            typer.echo(f"Error occurred while fetching pods: {e}")
        except FileNotFoundError:
            typer.echo("kubectl is not installed or not found in the system path.")

            
if __name__ == "__main__":
    app()