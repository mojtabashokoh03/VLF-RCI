# -*- coding: utf-8 -*-
"""
Phishing Detection - Comprehensive Feature Analysis
Compatible with Python 3.7
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_selection import SelectKBest, f_classif, RFECV
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, confusion_matrix,
                             classification_report)
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import json
import joblib
from functools import partial
from multiprocessing import Pool, cpu_count
import gc

# ============================================================================
# Configuration
# ============================================================================

FEATURE_GROUPS = {
    'URL': ['qty_dot_url', 'qty_hyphen_url', 'qty_underline_url', 'qty_slash_url',
            'qty_questionmark_url', 'qty_equal_url', 'qty_at_url', 'qty_and_url',
            'qty_exclamation_url', 'qty_space_url', 'qty_tilde_url', 'qty_comma_url',
            'qty_plus_url', 'qty_asterisk_url', 'qty_hashtag_url', 'qty_dollar_url',
            'qty_percent_url', 'qty_tld_url', 'length_url', 'email_in_url',
            'qty_dot_domain', 'qty_hyphen_domain', 'qty_underline_domain',
            'qty_slash_domain', 'qty_questionmark_domain', 'qty_equal_domain',
            'qty_at_domain', 'qty_and_domain', 'qty_exclamation_domain',
            'qty_space_domain', 'qty_tilde_domain', 'qty_comma_domain',
            'qty_plus_domain', 'qty_asterisk_domain', 'qty_hashtag_domain',
            'qty_dollar_domain', 'qty_percent_domain', 'qty_vowels_domain',
            'domain_length', 'domain_in_ip', 'server_client_domain',
            'qty_dot_directory', 'qty_hyphen_directory', 'qty_underline_directory',
            'qty_slash_directory', 'qty_questionmark_directory',
            'qty_equal_directory', 'qty_at_directory', 'qty_and_directory',
            'qty_exclamation_directory', 'qty_space_directory',
            'qty_tilde_directory', 'qty_comma_directory', 'qty_plus_directory',
            'qty_asterisk_directory', 'qty_hashtag_directory',
            'qty_dollar_directory', 'qty_percent_directory', 'directory_length',
            'qty_dot_file', 'qty_hyphen_file', 'qty_underline_file',
            'qty_slash_file', 'qty_questionmark_file', 'qty_equal_file',
            'qty_at_file', 'qty_and_file', 'qty_exclamation_file',
            'qty_space_file', 'qty_tilde_file', 'qty_comma_file',
            'qty_plus_file', 'qty_asterisk_file', 'qty_hashtag_file',
            'qty_dollar_file', 'qty_percent_file', 'file_length',
            'qty_dot_params', 'qty_hyphen_params', 'qty_underline_params',
            'qty_slash_params', 'qty_questionmark_params', 'qty_equal_params',
            'qty_at_params', 'qty_and_params', 'qty_exclamation_params',
            'qty_space_params', 'qty_tilde_params', 'qty_comma_params',
            'qty_plus_params', 'qty_asterisk_params', 'qty_hashtag_params',
            'qty_dollar_params', 'qty_percent_params', 'params_length',
            'tld_present_params', 'qty_params', 'hasssl', 'datessl',
            'freessl'],
    
    'HTML': ['hastaghtml', 'hastagbody', 'hastagiframe', 'inlink', 'outlink',
             'cssin', 'cssout', 'scriptin', 'scriptout', 'tedadmeta',
             'havmetakey', 'tedadkey', 'havemetarefresh',
             'havechangelocationbyjava', 'hasinputtext', 'hasinputpass',
             'hasinputemail', 'hasinputautoemail', 'hasinputautousername',
             'hasinputautoepassword', 'hasinputautoaddress', 'onclick', 'href',
             'onerror', 'onload', 'onmouseover', 'onfocus'],
    
    'HTMLCRWL': ['crawlhastaghtml', 'crawlhastagbody', 'crawlhastagiframe',
                 'crawlinlink', 'crawloutlink', 'crawlcssin', 'crawlcssout',
                 'crawlscriptin', 'crawlscriptout', 'crawltedadmeta',
                 'crawlhavmetakey', 'crawltedadkey', 'crawlhavemetarefresh',
                 'crawlhavechangelocationbyjava', 'crawlhasinputtext',
                 'crawlhasinputpass', 'crawlhasinputemail',
                 'crawlhasinputautoemail', 'crawlhasinputautousername',
                 'crawlhasinputautoepassword', 'crawlhasinputautoaddress',
                 'crawlonclick', 'crawlhref', 'crawlonerror', 'crawlonload',
                 'crawlonmouseover', 'crawlonfocus'],
    
    
    
    'VLF': ['VLF_num_blocks_1', 'VLF_largest_block_ratio_1', 'VLF_whitespace_ratio_1',
            'VLF_top_density_1', 'VLF_middle_density_1', 'VLF_bottom_density_1',
            'VLF_symmetry_score_1', 'VLF_edge_density_1', 'VLF_logo_x_1',
            'VLF_logo_y_1', 'VLF_logo_area_1', 'VLF_num_blocks_2',
            'VLF_largest_block_ratio_2', 'VLF_whitespace_ratio_2',
            'VLF_top_density_2', 'VLF_middle_density_2', 'VLF_bottom_density_2',
            'VLF_symmetry_score_2', 'VLF_edge_density_2', 'VLF_logo_x_2',
            'VLF_logo_y_2', 'VLF_logo_area_2'],
    
    'RCI': ['RCI_1', 'RCI_C1_mean_saturation_1', 'RCI_C2_saturation_std_1',
            'RCI_C3_rgb_imbalance_1', 'RCI_C4_spatial_anomaly_1',
            'RCI_mean_R_1', 'RCI_mean_G_1', 'RCI_mean_B_1', 'RCI_D_RG_1',
            'RCI_D_GB_1', 'RCI_D_RB_1', 'RCI_2', 'RCI_C1_mean_saturation_2',
            'RCI_C2_saturation_std_2', 'RCI_C3_rgb_imbalance_2',
            'RCI_C4_spatial_anomaly_2', 'RCI_mean_R_2', 'RCI_mean_G_2',
            'RCI_mean_B_2', 'RCI_D_RG_2', 'RCI_D_GB_2', 'RCI_D_RB_2'],
        
    'SVD50': ['svd50R_1', 'svd50G_1', 'svd50B_1', 'svd50R_2',
              'svd50G_2', 'svd50B_2'],

    
}

# All features for initial model
ALL_FEATURES = []
for group in FEATURE_GROUPS.values():
    ALL_FEATURES.extend(group)

# Define feature sets for ablation study
ABLATION_SETS = {
    'Base (URL+HTML+HTMLCRWL+RANK+SVD50+VLF+RCI)': ALL_FEATURES,
    'Remove RCI': [f for f in ALL_FEATURES if f not in FEATURE_GROUPS['RCI']],
    'Remove VLF': [f for f in ALL_FEATURES if f not in FEATURE_GROUPS['VLF']],
    'Remove SVD50': [f for f in ALL_FEATURES if f not in FEATURE_GROUPS['SVD50']],
    'Remove URL': [f for f in ALL_FEATURES if f not in FEATURE_GROUPS['URL']],
    'Remove HTML': [f for f in ALL_FEATURES if f not in FEATURE_GROUPS['HTML']],
    'Remove HTMLCRWL': [f for f in ALL_FEATURES if f not in FEATURE_GROUPS['HTMLCRWL']],
    'Final (URL+HTML+HTMLCRWL+VLF+RCI)': [f for f in ALL_FEATURES 
                                               if f not in FEATURE_GROUPS['SVD50']]
}

# Models to evaluate
MODELS = {
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'Extra Trees': ExtraTreesClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    'AdaBoost': AdaBoostClassifier(n_estimators=100, random_state=42),
    'XGBoost': XGBClassifier(n_estimators=100, random_state=42, n_jobs=-1, use_label_encoder=False, eval_metric='logloss'),
    'LightGBM': LGBMClassifier(n_estimators=100, random_state=42, n_jobs=-1, verbose=-1)
}

# ============================================================================
# Utility Functions
# ============================================================================

def create_output_directory():
    """Create output directory with timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = f'phishing_results_{timestamp}'
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'plots'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'models'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'feature_selection'), exist_ok=True)
    return output_dir

def load_and_clean_data(filepath):
    """Load dataset and clean missing/infinite values"""
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    
    # Check if target column exists
    if 'isphish' not in df.columns:
        raise ValueError("Column 'isphish' not found in dataset!")
    
    # Separate features and target
    X = df.drop('isphish', axis=1)
    y = df['isphish']
    
    # Keep only features that exist in our feature groups
    available_features = [f for f in ALL_FEATURES if f in X.columns]
    print(f"Found {len(available_features)} out of {len(ALL_FEATURES)} expected features")
    
    X = X[available_features]
    
    # Handle missing values - replace with column mean
    X = X.replace([np.inf, -np.inf], np.nan)
    for col in X.columns:
        if X[col].isna().any():
            median_val = X[col].median()
            X[col] = X[col].fillna(median_val)
            if X[col].isna().any():
                X[col] = X[col].fillna(0)
    
    # Encode target if needed
    if y.dtype == 'object':
        le = LabelEncoder()
        y = le.fit_transform(y)
    
    print(f"Data shape: {X.shape}, Target distribution: {np.bincount(y)}")
    return X, y, available_features

def evaluate_model(model, X_train, X_test, y_train, y_test, model_name):
    """Evaluate a single model and return metrics"""
    # Train
    model.fit(X_train, y_train)
    
    # Predict
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
    
    # Metrics
    metrics = {
        'Model': model_name,
        'Accuracy': accuracy_score(y_test, y_pred),
        'Precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
        'Recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
        'F1_Weighted': f1_score(y_test, y_pred, average='weighted', zero_division=0),
        'F1_Macro': f1_score(y_test, y_pred, average='macro', zero_division=0),
        'F1_Binary': f1_score(y_test, y_pred, average='binary', zero_division=0),
    }
    
    if y_proba is not None:
        try:
            metrics['AUC'] = roc_auc_score(y_test, y_proba)
        except:
            metrics['AUC'] = 0
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1_weighted')
    metrics['CV_F1_Mean'] = cv_scores.mean()
    metrics['CV_F1_Std'] = cv_scores.std()
    
    return metrics, y_pred, model

def train_and_evaluate(X, y, feature_set_name, feature_cols, output_dir, is_feature_selection=False):
    """Train and evaluate all models on a given feature set"""
    results = []
    models_dict = {}
    predictions = {}
    
    # Split data
    X_subset = X[feature_cols] if isinstance(X, pd.DataFrame) else X[:, feature_cols]
    X_train, X_test, y_train, y_test = train_test_split(
        X_subset, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Evaluate each model
    for model_name, model in MODELS.items():
        print(f"  Training {model_name} on {feature_set_name}...")
        try:
            # Create a fresh model instance
            if model_name == 'Random Forest':
                m = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
            elif model_name == 'Decision Tree':
                m = DecisionTreeClassifier(random_state=42)
            elif model_name == 'Gradient Boosting':
                m = GradientBoostingClassifier(n_estimators=100, random_state=42)
            elif model_name == 'Extra Trees':
                m = ExtraTreesClassifier(n_estimators=100, random_state=42, n_jobs=-1)
            elif model_name == 'AdaBoost':
                m = AdaBoostClassifier(n_estimators=100, random_state=42)
            elif model_name == 'XGBoost':
                m = XGBClassifier(n_estimators=100, random_state=42, n_jobs=-1, 
                                  use_label_encoder=False, eval_metric='logloss')
            elif model_name == 'LightGBM':
                m = LGBMClassifier(n_estimators=100, random_state=42, n_jobs=-1, verbose=-1)
            else:
                m = model
            
            metrics, y_pred, trained_model = evaluate_model(
                m, X_train_scaled, X_test_scaled, y_train, y_test, model_name
            )
            metrics['Feature_Set'] = feature_set_name
            metrics['Num_Features'] = len(feature_cols)
            results.append(metrics)
            models_dict[model_name] = trained_model
            predictions[model_name] = y_pred
            
        except Exception as e:
            print(f"  Error with {model_name}: {str(e)}")
            continue
    
    return results, models_dict, predictions, scaler

# ============================================================================
# Feature Selection Functions
# ============================================================================

def filter_feature_selection(X, y, feature_names, output_dir):
    """Perform filter-based feature selection using SelectKBest"""
    print("\n" + "="*60)
    print("FILTER FEATURE SELECTION (SelectKBest)")
    print("="*60)
    
    # Use all features
    X_filter = X[feature_names] if isinstance(X, pd.DataFrame) else X
    
    selector = SelectKBest(f_classif, k='all')
    selector.fit(X_filter, y)
    
    # Get scores
    scores = pd.DataFrame({
        'Feature': feature_names,
        'Score': selector.scores_,
        'PValue': selector.pvalues_
    }).sort_values('Score', ascending=False)
    
    # Select top features
    top_k_values = [5, 10, 20, 30, 50, 100]
    selected_features_by_k = {}
    
    for k in top_k_values:
        if k <= len(feature_names):
            top_features = scores.head(k)['Feature'].tolist()
            selected_features_by_k[k] = top_features
    
    # Also select features with p-value < 0.05
    significant_features = scores[scores['PValue'] < 0.05]['Feature'].tolist()
    selected_features_by_k['significant'] = significant_features
    
    # Save scores
    scores.to_csv(os.path.join(output_dir, 'feature_selection', 'filter_scores.csv'), index=False)
    
    # Plot feature importance
    plt.figure(figsize=(12, 10))
    top_n = min(50, len(scores))
    top_scores = scores.head(top_n)
    plt.barh(top_scores['Feature'], top_scores['Score'])
    plt.xlabel('F-Score')
    plt.title('Top Feature Scores (Filter Method)')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'plots', 'filter_feature_scores.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    return selected_features_by_k, scores

def wrapper_feature_selection(X, y, feature_names, output_dir):
    """Perform wrapper-based feature selection using RFECV"""
    print("\n" + "="*60)
    print("WRAPPER FEATURE SELECTION (RFECV)")
    print("="*60)
    
    # Use Random Forest as estimator
    estimator = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
    
    # RFECV with 5-fold cross-validation
    rfecv = RFECV(estimator, step=5, cv=5, scoring='f1_weighted', n_jobs=-1, verbose=1)
    
    X_wrapper = X[feature_names] if isinstance(X, pd.DataFrame) else X
    rfecv.fit(X_wrapper, y)
    
    # Get selected features
    selected_mask = rfecv.support_
    selected_features = [feature_names[i] for i, selected in enumerate(selected_mask) if selected]
    
    # Get ranking
    ranking = pd.DataFrame({
        'Feature': feature_names,
        'Ranking': rfecv.ranking_,
        'Selected': selected_mask
    }).sort_values('Ranking')
    
    # Save ranking
    ranking.to_csv(os.path.join(output_dir, 'feature_selection', 'wrapper_ranking.csv'), index=False)
    
    # Plot CV scores
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(rfecv.cv_results_['mean_test_score']) + 1), 
             rfecv.cv_results_['mean_test_score'])
    plt.xlabel('Number of Features Selected')
    plt.ylabel('CV Score (F1-Weighted)')
    plt.title('RFECV - Feature Selection Performance')
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'plots', 'wrapper_rfecv_scores.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"RFECV selected {len(selected_features)} features")
    
    return selected_features, ranking

# ============================================================================
# Ablation Study
# ============================================================================

def run_ablation_study(X, y, feature_names, output_dir):
    """Run ablation study by removing feature groups"""
    print("\n" + "="*60)
    print("ABLATION STUDY")
    print("="*60)
    
    all_results = []
    
    # Update feature sets to only include available features
    available_feature_sets = {}
    for name, features in ABLATION_SETS.items():
        available_features = [f for f in features if f in feature_names]
        available_feature_sets[name] = available_features
        print(f"{name}: {len(available_features)} features")
    
    for set_name, features in available_feature_sets.items():
        print(f"\n--- Evaluating: {set_name} ---")
        if len(features) == 0:
            print(f"Skipping {set_name} - no features available")
            continue
        
        results, _, _, _ = train_and_evaluate(
            X, y, set_name, features, output_dir
        )
        all_results.extend(results)
    
    # Convert to DataFrame
    results_df = pd.DataFrame(all_results)
    
    # Save results
    results_df.to_csv(os.path.join(output_dir, 'ablation_study_results.csv'), index=False)
    
    # Create ablation comparison plots
    plot_ablation_results(results_df, output_dir)
    
    return results_df

def plot_ablation_results(results_df, output_dir):
    """Create plots for ablation study results"""
    # Group by feature set and get mean F1
    pivot = results_df.pivot_table(
        index='Feature_Set', 
        columns='Model', 
        values='F1_Weighted',
        aggfunc='mean'
    ).sort_values('Random Forest', ascending=False)
    
    # Heatmap
    plt.figure(figsize=(14, 10))
    sns.heatmap(pivot, annot=True, fmt='.3f', cmap='RdYlGn', center=0.7, 
                vmin=0.6, vmax=0.95, linewidths=0.5)
    plt.title('Ablation Study: F1-Score by Feature Set and Model')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'plots', 'ablation_heatmap.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # Bar plot for each model
    for model in pivot.columns:
        plt.figure(figsize=(12, 8))
        sorted_df = pivot[model].sort_values(ascending=True)
        bars = plt.barh(sorted_df.index, sorted_df.values, color='steelblue')
        
        # Color bars based on value
        for bar, val in zip(bars, sorted_df.values):
            if val < 0.75:
                bar.set_color('coral')
            elif val < 0.85:
                bar.set_color('gold')
            else:
                bar.set_color('lightgreen')
        
        plt.xlabel('F1-Weighted Score')
        plt.title(f'Ablation Study: {model}')
        plt.xlim(0.6, 1.0)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'plots', f'ablation_{model.replace(" ", "_")}.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()

# ============================================================================
# Feature Count vs F1 Score
# ============================================================================

def plot_feature_count_vs_f1(results_df, output_dir):
    """Plot F1 score vs number of features"""
    plt.figure(figsize=(12, 8))
    
    models = results_df['Model'].unique()
    colors = plt.cm.tab10(np.linspace(0, 1, len(models)))
    
    for model, color in zip(models, colors):
        model_data = results_df[results_df['Model'] == model]
        plt.scatter(model_data['Num_Features'], model_data['F1_Weighted'], 
                   label=model, alpha=0.7, s=80, color=color)
        
        # Trend line
        z = np.polyfit(model_data['Num_Features'], model_data['F1_Weighted'], 1)
        p = np.poly1d(z)
        x_trend = np.linspace(model_data['Num_Features'].min(), model_data['Num_Features'].max(), 100)
        plt.plot(x_trend, p(x_trend), color=color, linestyle='--', alpha=0.5)
    
    plt.xlabel('Number of Features')
    plt.ylabel('F1-Weighted Score')
    plt.title('Feature Count vs F1-Score Across Models')
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'plots', 'feature_count_vs_f1.png'), dpi=300, bbox_inches='tight')
    plt.close()

# ============================================================================
# Feature Group Analysis
# ============================================================================

def analyze_feature_groups(X, y, feature_names, output_dir):
    """Analyze each feature group separately"""
    print("\n" + "="*60)
    print("FEATURE GROUP ANALYSIS")
    print("="*60)
    
    all_results = []
    
    # Define group combinations for testing
    combinations = {
        'URL only': FEATURE_GROUPS['URL'],
        'HTML only': FEATURE_GROUPS['HTML'],
        'HTMLCRWL only': FEATURE_GROUPS['HTMLCRWL'],
        'VLF only': FEATURE_GROUPS['VLF'],
        'RCI only': FEATURE_GROUPS['RCI'],
        'SVD50 only': FEATURE_GROUPS['SVD50'],
        'URL + HTML': FEATURE_GROUPS['URL'] + FEATURE_GROUPS['HTML'],
        'HTML + VLF + RCI': FEATURE_GROUPS['HTML'] + FEATURE_GROUPS['VLF'] + FEATURE_GROUPS['RCI'],
        'URL + VLF + RCI': FEATURE_GROUPS['URL']  + FEATURE_GROUPS['VLF'] + FEATURE_GROUPS['RCI'],
        'URL + HTML + VLF': FEATURE_GROUPS['URL'] + FEATURE_GROUPS['HTML'] + FEATURE_GROUPS['VLF'],
        'URL + HTML + RCI': FEATURE_GROUPS['URL'] + FEATURE_GROUPS['HTML']+ FEATURE_GROUPS['RCI'],
        'URL + HTML + HTMLCRWL': FEATURE_GROUPS['URL'] + FEATURE_GROUPS['HTML'] + FEATURE_GROUPS['HTMLCRWL'],
        'URL + HTML + HTMLCRWL + VLF': FEATURE_GROUPS['URL'] + FEATURE_GROUPS['HTML'] + FEATURE_GROUPS['HTMLCRWL'] + FEATURE_GROUPS['VLF'],
        'URL + HTML + HTMLCRWL + RCI': FEATURE_GROUPS['URL'] + FEATURE_GROUPS['HTML'] + FEATURE_GROUPS['HTMLCRWL'] + FEATURE_GROUPS['RCI'],
        'URL + HTML + HTMLCRWL + VLF + RCI': FEATURE_GROUPS['URL'] + FEATURE_GROUPS['HTML'] + FEATURE_GROUPS['HTMLCRWL'] + FEATURE_GROUPS['VLF'] + FEATURE_GROUPS['RCI'],
        'URL + HTML + VLF + RCI': FEATURE_GROUPS['URL'] + FEATURE_GROUPS['HTML'] + FEATURE_GROUPS['VLF'] + FEATURE_GROUPS['RCI'],
        'URL + HTML + HTMLCRWL + SVD50 + VLF + RCI (All)': ALL_FEATURES    }
    
    # Update combinations with available features
    valid_combinations = {}
    for name, features in combinations.items():
        available = [f for f in features if f in feature_names]
        if len(available) > 0:
            valid_combinations[name] = available
    
    for combo_name, features in valid_combinations.items():
        print(f"\n--- Evaluating: {combo_name} ({len(features)} features) ---")
        results, _, _, _ = train_and_evaluate(
            X, y, combo_name, features, output_dir
        )
        all_results.extend(results)
    
    results_df = pd.DataFrame(all_results)
    results_df.to_csv(os.path.join(output_dir, 'feature_group_analysis.csv'), index=False)
    
    # Create comparison plots
    plot_group_comparison(results_df, output_dir)
    
    return results_df

def plot_group_comparison(results_df, output_dir):
    """Plot comparison of feature group combinations"""
    # Pivot for heatmap
    pivot = results_df.pivot_table(
        index='Feature_Set', 
        columns='Model', 
        values='F1_Weighted',
        aggfunc='mean'
    )
    
    # Filter to meaningful combinations and sort
    pivot = pivot.sort_values('XGBoost', ascending=False)
    
    # Heatmap
    plt.figure(figsize=(16, 12))
    sns.heatmap(pivot, annot=True, fmt='.3f', cmap='RdYlGn', center=0.7,
                vmin=0.5, vmax=0.95, linewidths=0.5)
    plt.title('Feature Group Combinations: F1-Score Comparison')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'plots', 'group_comparison_heatmap.png'), 
               dpi=300, bbox_inches='tight')
    plt.close()
    
    # Bar plot with model average
    pivot['Mean_F1'] = pivot.mean(axis=1)
    pivot_sorted = pivot.sort_values('Mean_F1', ascending=True)
    
    plt.figure(figsize=(14, 10))
    bars = plt.barh(pivot_sorted.index, pivot_sorted['Mean_F1'], 
                   color='steelblue', edgecolor='black')
    
    # Color by value
    for bar, val in zip(bars, pivot_sorted['Mean_F1']):
        if val < 0.7:
            bar.set_color('coral')
        elif val < 0.8:
            bar.set_color('gold')
        elif val < 0.85:
            bar.set_color('lightgreen')
        else:
            bar.set_color('forestgreen')
    
    plt.xlabel('Mean F1-Weighted Score (Across Models)')
    plt.title('Feature Group Combinations Performance')
    plt.xlim(0.5, 1.0)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'plots', 'group_comparison_bar.png'), 
               dpi=300, bbox_inches='tight')
    plt.close()

# ============================================================================
# Final Model Evaluation
# ============================================================================

def evaluate_final_model(X, y, feature_names, output_dir):
    """Evaluate the final model with selected features"""
    print("\n" + "="*60)
    print("FINAL MODEL EVALUATION")
    print("="*60)
    
    # Final feature set: URL + HTML + HTMLCRWL + VLF + RCI (without SVD50)
    final_features = [f for f in feature_names if f not in FEATURE_GROUPS['SVD50']]
    print(f"Final features count: {len(final_features)}")
    
    # Also evaluate with all features for comparison
    all_features = feature_names
    
    final_results = []
    
    for name, features in [('All Features', all_features), ('Final (No SVD50)', final_features)]:
        print(f"\n--- Evaluating: {name} ---")
        results, models, preds, scaler = train_and_evaluate(
            X, y, name, features, output_dir
        )
        final_results.extend(results)
        
        # Save models
        for model_name, model in models.items():
            joblib.dump(model, os.path.join(output_dir, 'models', f'{model_name}_{name.replace(" ", "_")}.pkl'))
        
        # Save scaler
        joblib.dump(scaler, os.path.join(output_dir, 'models', f'scaler_{name.replace(" ", "_")}.pkl'))
    
    results_df = pd.DataFrame(final_results)
    results_df.to_csv(os.path.join(output_dir, 'final_results.csv'), index=False)
    
    # Create final comparison plots
    plot_final_comparison(results_df, output_dir)
    
    return results_df

def plot_final_comparison(results_df, output_dir):
    """Plot final model comparison"""
    # Group by feature set
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    feature_sets = results_df['Feature_Set'].unique()
    
    for idx, fs in enumerate(feature_sets):
        fs_data = results_df[results_df['Feature_Set'] == fs]
        models = fs_data['Model'].values
        f1_scores = fs_data['F1_Weighted'].values
        
        # Sort by F1
        sorted_idx = np.argsort(f1_scores)
        models_sorted = [models[i] for i in sorted_idx]
        f1_sorted = [f1_scores[i] for i in sorted_idx]
        
        colors = ['#2ecc71' if f >= 0.85 else '#f1c40f' if f >= 0.8 else '#e74c3c' for f in f1_sorted]
        
        axes[idx].barh(models_sorted, f1_sorted, color=colors, edgecolor='black')
        axes[idx].set_xlabel('F1-Weighted Score')
        axes[idx].set_title(f'{fs} - Model Comparison')
        axes[idx].set_xlim(0.7, 1.0)
        
        # Add value labels
        for i, v in enumerate(f1_sorted):
            axes[idx].text(v + 0.005, i, f'{v:.3f}', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'plots', 'final_model_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # Detailed metrics table
    metrics_cols = ['Model', 'Feature_Set', 'Accuracy', 'Precision', 'Recall', 
                    'F1_Weighted', 'F1_Macro', 'AUC', 'CV_F1_Mean', 'CV_F1_Std']
    metrics_df = results_df[metrics_cols].round(4)
    metrics_df.to_csv(os.path.join(output_dir, 'detailed_metrics.csv'), index=False)
    
    # Create a styled table image
    fig, ax = plt.subplots(figsize=(14, max(8, 0.5 * len(metrics_df))))
    ax.axis('off')
    table = ax.table(cellText=metrics_df.values,
                     colLabels=metrics_df.columns,
                     cellLoc='center',
                     loc='center',
                     colWidths=[0.12]*len(metrics_df.columns))
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.5)
    
    # Color cells
    for i, row in enumerate(metrics_df.values):
        for j, val in enumerate(row):
            if j >= 2 and val != '':
                if isinstance(val, (int, float)):
                    if val >= 0.85:
                        table[(i+1, j)].set_facecolor('#d4edda')
                    elif val >= 0.75:
                        table[(i+1, j)].set_facecolor('#fff3cd')
                    else:
                        table[(i+1, j)].set_facecolor('#f8d7da')
    
    plt.title('Detailed Model Metrics', fontsize=14, pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'plots', 'detailed_metrics_table.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()

# ============================================================================
# Main Execution
# ============================================================================

def main():
    print("="*70)
    print("PHISHING DETECTION - COMPREHENSIVE FEATURE ANALYSIS")
    print("="*70)
    print(f"Python Version: {os.sys.version}")
    
    # Create output directory
    output_dir = create_output_directory()
    print(f"\nResults will be saved to: {output_dir}")
    
    # Load and clean data
    X, y, available_features = load_and_clean_data('dataset.csv')
    
    # Save feature list
    with open(os.path.join(output_dir, 'available_features.txt'), 'w') as f:
        f.write('\n'.join(available_features))
    
    print(f"\nAvailable features: {len(available_features)}")
    
    # ========================================================================
    # 1. Run Ablation Study
    # ========================================================================
    ablation_results = run_ablation_study(X, y, available_features, output_dir)
    print("\nAblation Study Complete!")
    
    # ========================================================================
    # 2. Feature Count vs F1 Score Plot
    # ========================================================================
    plot_feature_count_vs_f1(ablation_results, output_dir)
    print("Feature Count vs F1 Plot Created!")
    
    # ========================================================================
    # 3. Feature Group Analysis
    # ========================================================================
    group_results = analyze_feature_groups(X, y, available_features, output_dir)
    print("Feature Group Analysis Complete!")
    
    # ========================================================================
    # 4. Filter Feature Selection
    # ========================================================================
    filter_selected, filter_scores = filter_feature_selection(
        X, y, available_features, output_dir
    )
    print("Filter Feature Selection Complete!")
    
    # ========================================================================
    # 5. Wrapper Feature Selection
    # ========================================================================
    wrapper_selected, wrapper_ranking = wrapper_feature_selection(
        X, y, available_features, output_dir
    )
    print("Wrapper Feature Selection Complete!")
    
    # ========================================================================
    # 6. Evaluate Selected Features from Wrapper
    # ========================================================================
    print("\n" + "="*60)
    print("EVALUATING WRAPPER SELECTED FEATURES")
    print("="*60)
    
    wrapper_results, _, _, _ = train_and_evaluate(
        X, y, 'Wrapper Selected Features', wrapper_selected, output_dir
    )
    wrapper_df = pd.DataFrame(wrapper_results)
    wrapper_df.to_csv(os.path.join(output_dir, 'wrapper_selected_results.csv'), index=False)
    
    # ========================================================================
    # 7. Evaluate Filter Selected Features (Top 50)
    # ========================================================================
    print("\n" + "="*60)
    print("EVALUATING FILTER SELECTED FEATURES (Top 50)")
    print("="*60)
    
    if len(available_features) >= 50:
        filter_top50 = filter_scores.head(50)['Feature'].tolist()
        filter_results, _, _, _ = train_and_evaluate(
            X, y, 'Filter Selected (Top 50)', filter_top50, output_dir
        )
        filter_df = pd.DataFrame(filter_results)
        filter_df.to_csv(os.path.join(output_dir, 'filter_selected_results.csv'), index=False)
    
    # ========================================================================
    # 8. Final Model Evaluation
    # ========================================================================
    final_results = evaluate_final_model(X, y, available_features, output_dir)
    print("Final Model Evaluation Complete!")
    
    # ========================================================================
    # 9. Summary Report
    # ========================================================================
    print("\n" + "="*70)
    print("SUMMARY REPORT")
    print("="*70)
    
    # Best model overall
    best_all = final_results.loc[final_results['F1_Weighted'].idxmax()]
    print(f"\nBest Model Overall: {best_all['Model']}")
    print(f"  Feature Set: {best_all['Feature_Set']}")
    print(f"  F1-Weighted: {best_all['F1_Weighted']:.4f}")
    print(f"  Accuracy: {best_all['Accuracy']:.4f}")
    print(f"  Precision: {best_all['Precision']:.4f}")
    print(f"  Recall: {best_all['Recall']:.4f}")
    print(f"  AUC: {best_all['AUC']:.4f}")
    
    # Best model per feature set
    print("\nBest Model per Feature Set:")
    for fs in final_results['Feature_Set'].unique():
        fs_best = final_results[final_results['Feature_Set'] == fs].loc[
            final_results[final_results['Feature_Set'] == fs]['F1_Weighted'].idxmax()
        ]
        print(f"  {fs}: {fs_best['Model']} (F1={fs_best['F1_Weighted']:.4f})")
    
    # Wrapper selection summary
    print(f"\nWrapper Feature Selection: {len(wrapper_selected)} features selected")
    print(f"  Top 10 features: {wrapper_selected[:10]}")
    
    print("\n" + "="*70)
    print(f"ALL RESULTS SAVED TO: {output_dir}")
    print("="*70)
    
    # Generate final report
    generate_report(output_dir, final_results, ablation_results, wrapper_selected, filter_scores)
    
    print("\nAnalysis Complete!")

def generate_report(output_dir, final_results, ablation_results, wrapper_selected, filter_scores):
    """Generate a comprehensive HTML report"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Phishing Detection - Feature Analysis Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
            h2 {{ color: #34495e; margin-top: 30px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th {{ background: #3498db; color: white; padding: 12px; text-align: left; }}
            td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
            tr:hover {{ background: #f5f5f5; }}
            .metric-good {{ color: #27ae60; font-weight: bold; }}
            .metric-medium {{ color: #f39c12; font-weight: bold; }}
            .metric-bad {{ color: #e74c3c; font-weight: bold; }}
            .highlight {{ background: #fef9e7; padding: 15px; border-left: 4px solid #f1c40f; }}
            .feature-list {{ column-count: 4; column-gap: 20px; }}
            .feature-list li {{ break-inside: avoid; padding: 3px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>?? Phishing Detection - Feature Analysis Report</h1>
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <h2>?? Best Model Performance</h2>
            {final_results.loc[[final_results['F1_Weighted'].idxmax()]].to_html()}
            
            <h2>?? Ablation Study - Best Feature Set</h2>
            <div class="highlight">
                <p><strong>Best Performing Feature Set:</strong> {ablation_results.groupby('Feature_Set')['F1_Weighted'].mean().idxmax()}</p>
                <p><strong>Mean F1 Score:</strong> {ablation_results.groupby('Feature_Set')['F1_Weighted'].mean().max():.4f}</p>
            </div>
            
            <h2>? Wrapper Feature Selection</h2>
            <p><strong>Number of Features Selected:</strong> {len(wrapper_selected)}</p>
            <p><strong>Top 20 Features:</strong></p>
            <ul class="feature-list">
                {"".join([f"<li>{f}</li>" for f in wrapper_selected[:20]])}
            </ul>
            
            <h2>?? Model Performance Summary</h2>
            {final_results[['Model', 'Feature_Set', 'Accuracy', 'F1_Weighted', 'AUC']].round(4).to_html(index=False)}
            
            <h2>??? Plots</h2>
            <p>The following plots are available in the <code>plots/</code> directory:</p>
            <ul>
                <li><code>ablation_heatmap.png</code> - Ablation study heatmap</li>
                <li><code>feature_count_vs_f1.png</code> - Feature count vs F1 score</li>
                <li><code>group_comparison_heatmap.png</code> - Feature group comparison</li>
                <li><code>final_model_comparison.png</code> - Final model comparison</li>
                <li><code>filter_feature_scores.png</code> - Filter feature scores</li>
                <li><code>wrapper_rfecv_scores.png</code> - Wrapper RFECV scores</li>
            </ul>
            
            <h2>?? Output Files</h2>
            <ul>
                <li><code>ablation_study_results.csv</code> - Full ablation study results</li>
                <li><code>feature_group_analysis.csv</code> - Feature group combination results</li>
                <li><code>final_results.csv</code> - Final model evaluation results</li>
                <li><code>detailed_metrics.csv</code> - Detailed metrics for all models</li>
                <li><code>filter_scores.csv</code> - Filter feature selection scores</li>
                <li><code>wrapper_ranking.csv</code> - Wrapper feature ranking</li>
            </ul>
            
            <p style="margin-top: 40px; color: #7f8c8d; text-align: center;">
                Report generated by Phishing Detection Feature Analysis Pipeline
            </p>
        </div>
    </body>
    </html>
    """
    
    with open(os.path.join(output_dir, 'report.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    main()