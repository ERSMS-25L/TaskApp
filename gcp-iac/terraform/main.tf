variable "project_id" {
  type    = string
  default = "ersms-25l-462511"
}

variable "region" {
  type    = string
  default = "europe-central2"
}

variable "cluster_name" {
  type    = string
  default = "ersms-cluster"
}

resource "google_container_cluster" "primary" {
  name               = var.cluster_name
  location           = var.region
  initial_node_count = 1
  deletion_protection = false  # Disable deletion protection
  node_config {
    machine_type = "e2-small"
    disk_size_gb = 20  # Reduced disk size
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}

resource "google_container_node_pool" "primary_nodes" {
  cluster    = google_container_cluster.primary.name
  location   = google_container_cluster.primary.location
  node_count = 1

  node_config {
    preemptible  = true
    machine_type = "e2-small"
    disk_size_gb = 20  # Reduced disk size for each node in the pool
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}

output "kubernetes_cluster_name" {
  value = google_container_cluster.primary.name
}
