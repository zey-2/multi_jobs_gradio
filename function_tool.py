"""
Function Tools for Job Search
=============================
This module provides utility functions for job search operations using both FindSGJobs and Adzuna APIs.

Functions:
- search_jobs_api: Search for jobs with detailed information (FindSGJobs)
- calculate_job_statistics: Get aggregated statistics about job market (FindSGJobs)
- search_adzuna_jobs: Search for jobs using Adzuna API
- get_adzuna_histogram: Get salary distribution data from Adzuna
- get_adzuna_top_companies: Get top hiring companies from Adzuna

Author: ADK Demo
Date: November 13, 2025
"""

import os
import requests
from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
import re


def search_jobs_api(keywords: str, page: int = 1, per_page_count: int = 10) -> Dict[str, Any]:
    """
    Search for jobs using the FindSGJobs API.

    Args:
        keywords: Search keywords (e.g., "cook", "engineer", "manager")
        page: Page number (default: 1)
        per_page_count: Number of results per page (default: 10, max: 20)

    Returns:
        dict: Structured job search results with success status
    """
    base_url = "https://www.findsgjobs.com/apis/job/searchable"

    params = {
        "page": page,
        "per_page_count": min(per_page_count, 20),
        "keywords": keywords
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        json_response = response.json()

        # Extract and structure job data
        jobs = []
        total_count = 0
        current_page = page
        total_pages = 0

        if "data" in json_response:
            data = json_response["data"]

            # Get pagination info
            if "pager" in data:
                pager = data["pager"]
                total_count = pager.get("record_count", 0)
                current_page = pager.get("page", page)
                total_pages = pager.get("page_count", 0)

            # Extract job details
            if "result" in data:
                for item in data["result"]:
                    job = item.get('job', {})
                    company = item.get('company', {})

                    # Extract salary information
                    salary_info = None
                    if not job.get('id_Job_Donotdisplaysalary', 0):
                        salary_range = job.get('Salaryrange', {}).get('caption')
                        if salary_range:
                            currency = job.get('id_Job_Currency', {}).get('caption', 'SGD')
                            interval = job.get('id_Job_Interval', {}).get('caption', 'Month')
                            salary_info = f"{currency} {salary_range} per {interval}"

                    # Extract description (clean HTML)
                    description = job.get('JobDescription', '')
                    if description:
                        soup = BeautifulSoup(description, 'html.parser')
                        plain_text = soup.get_text()
                        plain_text = re.sub(r'\n+', '\n', plain_text).strip()
                        description = plain_text[:500] + '...' if len(plain_text) > 500 else plain_text

                    job_info = {
                        "job_id": job.get('id', ''),
                        "title": job.get('Title', 'N/A'),
                        "company": company.get('CompanyName', 'N/A'),
                        "url": f"https://www.findsgjobs.com/job/{job.get('id', '')}" if job.get('id') else '',
                        "categories": [cat.get('caption', '') for cat in job.get('JobCategory', [])],
                        "employment_type": [et.get('caption', '') for et in job.get('EmploymentType', [])],
                        "location": [mrt.get('caption', '') for mrt in job.get('id_Job_NearestMRTStation', [])],
                        "salary": salary_info,
                        "experience": job.get('MinimumYearsofExperience', {}).get('caption', 'N/A'),
                        "education": job.get('MinimumEducationLevel', {}).get('caption', 'N/A'),
                        "position_level": job.get('id_Job_PositionLevel', {}).get('caption', 'N/A'),
                        "work_arrangement": job.get('id_Job_WorkArrangement', {}).get('caption', 'N/A'),
                        "skills": job.get('id_Job_Skills', []),
                        "posted_date": job.get('activation_date', 'N/A'),
                        "expires_date": job.get('expiration_date', 'N/A'),
                        "description": description
                    }

                    jobs.append(job_info)

        return {
            "success": True,
            "total_jobs": total_count,
            "current_page": current_page,
            "total_pages": total_pages,
            "results_on_page": len(jobs),
            "jobs": jobs
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"API request failed: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }


def calculate_job_statistics(keywords: str, sample_size: int = 20) -> Dict[str, Any]:
    """
    Get statistical summary of job search results.

    Args:
        keywords: Search keywords
        sample_size: Number of jobs to analyze (max 20)

    Returns:
        dict: Job market statistics with success status
    """
    # Get job listings
    result = search_jobs_api(keywords, page=1, per_page_count=min(sample_size, 20))

    if not result.get("success"):
        return result

    jobs = result.get("jobs", [])
    total_jobs = result.get("total_jobs", 0)

    # Compute statistics
    category_counts = {}
    employment_type_counts = {}
    location_counts = {}
    education_counts = {}
    experience_counts = {}

    for job in jobs:
        # Count categories
        for category in job.get("categories", []):
            if category:
                category_counts[category] = category_counts.get(category, 0) + 1

        # Count employment types
        for emp_type in job.get("employment_type", []):
            if emp_type:
                employment_type_counts[emp_type] = employment_type_counts.get(emp_type, 0) + 1

        # Count locations
        for location in job.get("location", []):
            if location:
                location_counts[location] = location_counts.get(location, 0) + 1

        # Count education levels
        education = job.get("education")
        if education and education != "N/A":
            education_counts[education] = education_counts.get(education, 0) + 1

        # Count experience levels
        experience = job.get("experience")
        if experience and experience != "N/A":
            experience_counts[experience] = experience_counts.get(experience, 0) + 1

    return {
        "success": True,
        "keyword": keywords,
        "total_jobs_in_market": total_jobs,
        "jobs_analyzed": len(jobs),
        "statistics": {
            "top_categories": dict(sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
            "employment_types": employment_type_counts,
            "top_locations": dict(sorted(location_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
            "education_requirements": education_counts,
            "experience_requirements": experience_counts
        }
    }


# ========================================
# ADZUNA API FUNCTIONS
# ========================================

def search_adzuna_jobs(
    what: str,
    where: str = "Singapore",
    page: int = 1,
    results_per_page: int = 5,
    sort_by: str = "relevance",
    category: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for jobs using the Adzuna API.

    Args:
        what: Job title or keywords (e.g., "data analyst", "software engineer")
        where: Location (default: "Singapore")
        page: Page number (default: 1)
        results_per_page: Number of results per page (default: 5, max: 50)
        sort_by: Sort order - "relevance", "date", or "salary" (default: "relevance")
        category: Optional job category filter

    Returns:
        dict: Structured job search results with success status
    """
    app_id = os.environ.get("ADZUNA_APP_ID")
    app_key = os.environ.get("ADZUNA_APP_KEY")
    
    if not app_id or not app_key:
        return {
            "success": False,
            "error": "ADZUNA_APP_ID and ADZUNA_APP_KEY environment variables must be set. Get your credentials from https://developer.adzuna.com/"
        }
    
    # Adzuna uses country codes; map common names to codes
    country_code = "sg"  # Singapore
    if where.lower() in ["uk", "united kingdom", "gb"]:
        country_code = "gb"
    elif where.lower() in ["us", "usa", "united states"]:
        country_code = "us"
    elif where.lower() in ["au", "australia"]:
        country_code = "au"
    
    base_url = f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/{page}"
    
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": min(results_per_page, 50),
        "what": what,
        "where": where if country_code == "sg" else "",  # For Singapore, we can specify area
        "sort_by": sort_by
    }
    
    if category:
        params["category"] = category
    
    try:
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        json_response = response.json()
        
        # Extract and structure job data
        jobs = []
        results = json_response.get("results", [])
        
        for job in results:
            job_info = {
                "job_id": job.get("id", ""),
                "title": job.get("title", "N/A"),
                "company": job.get("company", {}).get("display_name", "N/A"),
                "location": job.get("location", {}).get("display_name", "N/A"),
                "description": job.get("description", "")[:500] + "..." if len(job.get("description", "")) > 500 else job.get("description", ""),
                "created": job.get("created", "N/A"),
                "contract_type": job.get("contract_type", "N/A"),
                "contract_time": job.get("contract_time", "N/A"),
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max"),
                "salary_is_predicted": job.get("salary_is_predicted", False),
                "redirect_url": job.get("redirect_url", ""),
                "category": job.get("category", {}).get("label", "N/A"),
                "latitude": job.get("latitude"),
                "longitude": job.get("longitude")
            }
            jobs.append(job_info)
        
        return {
            "success": True,
            "total_results": json_response.get("count", 0),
            "current_page": page,
            "results_on_page": len(jobs),
            "mean_salary": json_response.get("mean", 0),
            "jobs": jobs
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"API request failed: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }


def get_adzuna_histogram(
    location: str = "Singapore",
    category: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get salary distribution histogram from Adzuna.

    Args:
        location: Location to get salary data for (default: "Singapore")
        category: Optional job category filter

    Returns:
        dict: Salary distribution data with success status
    """
    app_id = os.environ.get("ADZUNA_APP_ID")
    app_key = os.environ.get("ADZUNA_APP_KEY")
    
    if not app_id or not app_key:
        return {
            "success": False,
            "error": "ADZUNA_APP_ID and ADZUNA_APP_KEY environment variables must be set"
        }
    
    country_code = "sg"
    base_url = f"https://api.adzuna.com/v1/api/jobs/{country_code}/histogram"
    
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "location0": location
    }
    
    if category:
        params["category"] = category
    
    try:
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        json_response = response.json()
        
        return {
            "success": True,
            "histogram": json_response.get("histogram", {}),
            "location": location,
            "category": category
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"API request failed: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }


def get_adzuna_top_companies(
    location: str = "Singapore"
) -> Dict[str, Any]:
    """
    Get top hiring companies from Adzuna.

    Args:
        location: Location to get company data for (default: "Singapore")

    Returns:
        dict: Top companies data with success status
    """
    app_id = os.environ.get("ADZUNA_APP_ID")
    app_key = os.environ.get("ADZUNA_APP_KEY")
    
    if not app_id or not app_key:
        return {
            "success": False,
            "error": "ADZUNA_APP_ID and ADZUNA_APP_KEY environment variables must be set"
        }
    
    country_code = "sg"
    base_url = f"https://api.adzuna.com/v1/api/jobs/{country_code}/top_companies"
    
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "location0": location
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        json_response = response.json()
        
        return {
            "success": True,
            "top_companies": json_response.get("leaderboard", []),
            "location": location
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"API request failed: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }
