import pandas as pd
import numpy as np
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score, classification_report
from xgboost import XGBClassifier
import time
import warnings
warnings.filterwarnings('ignore')

# ==================== 1. LOAD DATA ====================
print("Loading data...")
df = pd.read_csv('dataset.csv')

# ==================== 2. FEATURE SELECTION ====================
features = ['qty_dot_url', 'qty_hyphen_url', 'qty_underline_url', 'qty_slash_url', 
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
            'freessl','hastaghtml', 'hastagbody', 'hastagiframe', 'inlink', 'outlink',
            'cssin', 'cssout', 'scriptin', 'scriptout', 'tedadmeta',
            'havmetakey', 'tedadkey', 'havemetarefresh',
            'havechangelocationbyjava', 'hasinputtext', 'hasinputpass',
            'hasinputemail', 'hasinputautoemail', 'hasinputautousername',
            'hasinputautoepassword', 'hasinputautoaddress', 'onclick', 'href',
            'onerror', 'onload', 'onmouseover', 'onfocus','crawlhastaghtml', 'crawlhastagbody', 'crawlhastagiframe',
                 'crawlinlink', 'crawloutlink', 'crawlcssin', 'crawlcssout',
                 'crawlscriptin', 'crawlscriptout', 'crawltedadmeta',
                 'crawlhavmetakey', 'crawltedadkey', 'crawlhavemetarefresh',
                 'crawlhavechangelocationbyjava', 'crawlhasinputtext',
                 'crawlhasinputpass', 'crawlhasinputemail',
                 'crawlhasinputautoemail', 'crawlhasinputautousername',
                 'crawlhasinputautoepassword', 'crawlhasinputautoaddress',
                 'crawlonclick', 'crawlhref', 'crawlonerror', 'crawlonload',
                 'crawlonmouseover', 'crawlonfocus','VLF_num_blocks_1', 'VLF_largest_block_ratio_1', 'VLF_whitespace_ratio_1',
            'VLF_top_density_1', 'VLF_middle_density_1', 'VLF_bottom_density_1',
            'VLF_symmetry_score_1', 'VLF_edge_density_1', 'VLF_logo_x_1',
            'VLF_logo_y_1', 'VLF_logo_area_1', 'VLF_num_blocks_2',
            'VLF_largest_block_ratio_2', 'VLF_whitespace_ratio_2',
            'VLF_top_density_2', 'VLF_middle_density_2', 'VLF_bottom_density_2',
            'VLF_symmetry_score_2', 'VLF_edge_density_2', 'VLF_logo_x_2',
            'VLF_logo_y_2', 'VLF_logo_area_2','RCI_1', 'RCI_C1_mean_saturation_1', 'RCI_C2_saturation_std_1',
            'RCI_C3_rgb_imbalance_1', 'RCI_C4_spatial_anomaly_1',
            'RCI_mean_R_1', 'RCI_mean_G_1', 'RCI_mean_B_1', 'RCI_D_RG_1',
            'RCI_D_GB_1', 'RCI_D_RB_1', 'RCI_2', 'RCI_C1_mean_saturation_2',
            'RCI_C2_saturation_std_2', 'RCI_C3_rgb_imbalance_2',
            'RCI_C4_spatial_anomaly_2', 'RCI_mean_R_2', 'RCI_mean_G_2',
            'RCI_mean_B_2', 'RCI_D_RG_2', 'RCI_D_GB_2', 'RCI_D_RB_2']

existing_features = [f for f in features if f in df.columns]
print(f"Using {len(existing_features)} features out of {len(features)}")

X = df[existing_features]
y = df['isphish']

# ==================== 3. HANDLE MISSING & INF VALUES ====================
print("Cleaning data...")
X = X.replace([np.inf, -np.inf], np.nan)
for col in X.columns:
    if X[col].isna().any():
        median_val = X[col].median()
        X[col] = X[col].fillna(median_val)
        if X[col].isna().any():
            X[col] = X[col].fillna(0)

X = X.loc[:, X.std() > 0]
print(f"Features after cleaning: {X.shape[1]}")

# ==================== 4. MODEL DEFINITION ====================
model = XGBClassifier(n_estimators=100, random_state=42, n_jobs=-1, 
                      use_label_encoder=False, eval_metric='logloss')

# ==================== 5. NORMAL MODE (NO CROSS-VALIDATION) ====================
print("\n" + "="*80)
print("NORMAL MODE (Training on full dataset, testing on full dataset)")
print("="*80)

start_time = time.time()
model.fit(X, y)
y_pred = model.predict(X)
y_pred_proba = model.predict_proba(X)[:, 1]

# Calculate metrics
normal_metrics = {
    'Accuracy': accuracy_score(y, y_pred),
    'F1-Score': f1_score(y, y_pred),
    'Precision': precision_score(y, y_pred),
    'Recall': recall_score(y, y_pred),
    'ROC-AUC': roc_auc_score(y, y_pred_proba)
}

elapsed_time = time.time() - start_time

print(f"\nResults on Full Dataset (Training + Testing):")
print("-" * 40)
for metric, value in normal_metrics.items():
    print(f"{metric}: {value:.4f}")
print(f"Time: {elapsed_time:.2f} seconds")

# ==================== 6. TRAIN-TEST SPLIT MODE ====================
print("\n" + "="*80)
print("TRAIN-TEST SPLIT MODE (70-30 split)")
print("="*80)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

start_time = time.time()
model_split = XGBClassifier(n_estimators=100, random_state=42, n_jobs=-1,
                           use_label_encoder=False, eval_metric='logloss')
model_split.fit(X_train, y_train)
y_pred_test = model_split.predict(X_test)
y_pred_proba_test = model_split.predict_proba(X_test)[:, 1]

split_metrics = {
    'Accuracy': accuracy_score(y_test, y_pred_test),
    'F1-Score': f1_score(y_test, y_pred_test),
    'Precision': precision_score(y_test, y_pred_test),
    'Recall': recall_score(y_test, y_pred_test),
    'ROC-AUC': roc_auc_score(y_test, y_pred_proba_test)
}

elapsed_time = time.time() - start_time

print(f"\nResults on Test Set (70-30 split):")
print("-" * 40)
for metric, value in split_metrics.items():
    print(f"{metric}: {value:.4f}")
print(f"Time: {elapsed_time:.2f} seconds")

# ==================== 7. CROSS-VALIDATION STRATEGIES ====================
cv_strategies = {
    'KFold_5': KFold(n_splits=5, shuffle=True, random_state=42),
    'KFold_10': KFold(n_splits=10, shuffle=True, random_state=42),
    'StratifiedKFold_5': StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    'StratifiedKFold_10': StratifiedKFold(n_splits=10, shuffle=True, random_state=42),
}

# Different random states for additional variation
random_states = [0, 1, 2, 3, 4, 5, 10, 20, 42, 100]

# ==================== 8. RUN EXPERIMENTS ====================
results = []

# Add normal mode results
for metric, value in normal_metrics.items():
    results.append({
        'Mode': 'Normal_FullData',
        'CV_Strategy': 'Full Dataset',
        'Random_State': 'N/A',
        'Metric': metric,
        'Mean_Score': value,
        'Std_Score': 0,
        'Time_Seconds': elapsed_time
    })

# Add train-test split results
for metric, value in split_metrics.items():
    results.append({
        'Mode': 'TrainTest_Split',
        'CV_Strategy': '70-30 Split',
        'Random_State': '42',
        'Metric': metric,
        'Mean_Score': value,
        'Std_Score': 0,
        'Time_Seconds': elapsed_time
    })

# Run for each CV strategy
for cv_name, cv in cv_strategies.items():
    print(f"\nRunning {cv_name}...")
    start_time = time.time()
    
    # Cross-validation with multiple metrics
    scoring = ['accuracy', 'f1', 'precision', 'recall', 'roc_auc']
    cv_results = cross_validate(model, X, y, cv=cv, scoring=scoring, 
                               return_train_score=False, n_jobs=-1)
    
    elapsed_time = time.time() - start_time
    
    # Store results
    for metric in scoring:
        results.append({
            'Mode': 'CV',
            'CV_Strategy': cv_name,
            'Random_State': 'default',
            'Metric': metric,
            'Mean_Score': np.mean(cv_results[f'test_{metric}']),
            'Std_Score': np.std(cv_results[f'test_{metric}']),
            'Time_Seconds': elapsed_time
        })
    
    print(f"{cv_name} completed in {elapsed_time:.2f} seconds")

# Run with different random states for StratifiedKFold 5 and 10
for random_state in random_states:
    for n_splits in [5, 10]:
        cv_name = f'StratifiedKFold_{n_splits}_RS{random_state}'
        print(f"\nRunning {cv_name}...")
        
        cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
        model_temp = XGBClassifier(n_estimators=100, random_state=random_state, 
                                  n_jobs=-1, use_label_encoder=False, 
                                  eval_metric='logloss')
        
        start_time = time.time()
        scoring = ['accuracy', 'f1', 'precision', 'recall', 'roc_auc']
        cv_results = cross_validate(model_temp, X, y, cv=cv, scoring=scoring,
                                   return_train_score=False, n_jobs=-1)
        elapsed_time = time.time() - start_time
        
        for metric in scoring:
            results.append({
                'Mode': 'CV',
                'CV_Strategy': f'StratifiedKFold_{n_splits}',
                'Random_State': random_state,
                'Metric': metric,
                'Mean_Score': np.mean(cv_results[f'test_{metric}']),
                'Std_Score': np.std(cv_results[f'test_{metric}']),
                'Time_Seconds': elapsed_time
            })

# ==================== 9. CREATE RESULTS TABLE ====================
results_df = pd.DataFrame(results)

# Pivot table for better visualization
pivot_table = results_df.pivot_table(
    index=['Mode', 'CV_Strategy', 'Random_State'], 
    columns='Metric', 
    values=['Mean_Score', 'Std_Score']
)

# Format the pivot table
pivot_table.columns = [f'{metric}_{stat}' for stat, metric in pivot_table.columns]
pivot_table = pivot_table.round(4)

# Add time information
time_table = results_df.groupby(['Mode', 'CV_Strategy', 'Random_State'])['Time_Seconds'].first().round(2)
pivot_table['Time_Seconds'] = time_table

# Sort the table
pivot_table = pivot_table.sort_index()

# ==================== 10. DISPLAY RESULTS ====================
print("\n" + "="*80)
print("COMPLETE RESULTS TABLE")
print("="*80)
print("\nAll Results (Mean +/- Std):")
print(pivot_table)

# Save to CSV
pivot_table.to_csv('xgboost_all_results.csv')
print(f"\nResults saved to 'xgboost_all_results.csv'")

# ==================== 11. SUMMARY COMPARISON ====================
print("\n" + "="*80)
print("SUMMARY COMPARISON")
print("="*80)

# Create comparison table for main metrics
comparison_data = []
for mode in ['Normal_FullData', 'TrainTest_Split']:
    for metric in ['Accuracy', 'F1-Score', 'Precision', 'Recall', 'ROC-AUC']:
        value = results_df[(results_df['Mode'] == mode) & (results_df['Metric'] == metric)]['Mean_Score'].values[0]
        comparison_data.append({
            'Mode': mode,
            'Metric': metric,
            'Score': value
        })

# Add best CV results
for metric in ['accuracy', 'f1', 'precision', 'recall', 'roc_auc']:
    best_cv = results_df[(results_df['Mode'] == 'CV') & (results_df['Metric'] == metric)]
    best_idx = best_cv['Mean_Score'].idxmax()
    best_row = best_cv.loc[best_idx]
    comparison_data.append({
        'Mode': f"Best_CV_{best_row['CV_Strategy']}",
        'Metric': metric.capitalize(),
        'Score': best_row['Mean_Score']
    })

comparison_df = pd.DataFrame(comparison_data)
comparison_pivot = comparison_df.pivot(index='Mode', columns='Metric', values='Score').round(4)
print("\nComparison of Different Approaches:")
print(comparison_pivot)

# ==================== 12. DETAILED METRICS PER MODE ====================
print("\n" + "="*80)
print("DETAILED METRICS PER EVALUATION MODE")
print("="*80)

# Normal mode details
print("\n[1] Normal Mode (Full Dataset):")
print("-" * 40)
for metric, value in normal_metrics.items():
    print(f"  {metric}: {value:.4f}")

# Train-Test split details
print("\n[2] Train-Test Split Mode (70-30):")
print("-" * 40)
for metric, value in split_metrics.items():
    print(f"  {metric}: {value:.4f}")

# CV mode details
print("\n[3] Cross-Validation Modes (Mean +/- Std):")
print("-" * 40)
for cv_name in ['KFold_5', 'KFold_10', 'StratifiedKFold_5', 'StratifiedKFold_10']:
    print(f"\n  {cv_name}:")
    subset = results_df[(results_df['Mode'] == 'CV') & (results_df['CV_Strategy'] == cv_name)]
    for metric in ['accuracy', 'f1', 'precision', 'recall', 'roc_auc']:
        row = subset[subset['Metric'] == metric]
        if not row.empty:
            mean_val = row['Mean_Score'].values[0]
            std_val = row['Std_Score'].values[0]
            print(f"    {metric.upper()}: {mean_val:.4f} +/- {std_val:.4f}")

# ==================== 13. VISUALIZATION (OPTIONAL) ====================
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Create comparison plot
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('XGBoost Performance Comparison', fontsize=16)
    
    metrics_to_plot = ['accuracy', 'f1', 'precision', 'recall', 'roc_auc']
    plot_data = results_df[results_df['Mode'] == 'CV'].copy()
    
    for idx, metric in enumerate(metrics_to_plot):
        ax = axes[idx // 2, idx % 2]
        subset = plot_data[plot_data['Metric'] == metric]
        
        # Bar plot for CV strategies
        cv_means = subset.groupby('CV_Strategy')['Mean_Score'].mean().sort_values()
        cv_stds = subset.groupby('CV_Strategy')['Std_Score'].mean()
        
        bars = ax.bar(cv_means.index, cv_means.values, yerr=cv_stds.values, capsize=5)
        ax.set_title(f'{metric.upper()}')
        ax.set_ylabel('Score')
        ax.set_ylim(0.7, 1.0)
        ax.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, val in zip(bars, cv_means.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                   f'{val:.3f}', ha='center', va='bottom', fontsize=8)
    
    # Add normal mode results as horizontal lines
    for idx, metric in enumerate(['accuracy', 'f1', 'precision', 'recall', 'roc_auc']):
        ax = axes[idx // 2, idx % 2]
        metric_key = {'accuracy': 'Accuracy', 'f1': 'F1-Score', 'precision': 'Precision', 
                      'recall': 'Recall', 'roc_auc': 'ROC-AUC'}[metric]
        
        if metric_key in normal_metrics:
            ax.axhline(y=normal_metrics[metric_key], color='red', linestyle='--', 
                      label=f'Full Data: {normal_metrics[metric_key]:.3f}')
        
        if metric_key in split_metrics:
            ax.axhline(y=split_metrics[metric_key], color='green', linestyle=':', 
                      label=f'70-30 Split: {split_metrics[metric_key]:.3f}')
        
        ax.legend(fontsize=7)
    
    plt.tight_layout()
    plt.savefig('xgboost_performance_comparison.png', dpi=300, bbox_inches='tight')
    print("\nVisualization saved as 'xgboost_performance_comparison.png'")
    plt.show()
    
except ImportError:
    print("\nMatplotlib/Seaborn not available. Skipping visualization.")